from fastapi import APIRouter, Depends, status, HTTPException, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.user import UserResponse, UserModel, TokenModel, RequestEmail
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(body: UserModel, background_tasks: BackgroundTasks, request: Request,
                  db: AsyncSession = Depends(get_db)):
    """
    The sign_up function creates a new user in the database.
    It takes a UserModel object as input, which is validated by pydantic.
    If the email address already exists in the database, an HTTP 409 Conflict error is raised.
    The password field of the UserModel object is hashed using Argon2 and stored in that form.
    A new user record is created with this data and returned to the caller.

    :param body: UserModel: Get the data from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base url of the request
    :param db: AsyncSession: Get the database session
    :return: The created user
    :doc-author: Trelent
    """
    if await repository_users.get_user_by_email(body.email, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    The login function is used to authenticate a user.
        It takes the username and password from the request body,
        verifies that they are correct, and returns an access token.

    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: AsyncSession: Get the database session
    :return: A token
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if auth_service.verify_password(body.password, user.password):
        access_token = await auth_service.create_access_token(data={"sub": user.email})
        refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
        await repository_users.update_token(user, refresh_token, db)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security),
                        db: AsyncSession = Depends(get_db)):
    """
    The refresh_token function is used to refresh the access token.
    It takes in a refresh token and returns a new pair of access and refresh tokens.
    The function first decodes the refresh_token to get the email of user, then it gets that user from database,
    and checks if their current stored refresh_token matches with what was passed in as argument. If not, it raises an
    error 401 Unauthorized. If they match, we create new tokens for them and update their stored tokens.

    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: AsyncSession: Access the database
    :return: A new access token and refresh token
    :doc-author: Trelent
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/confirmed_email/{token}", status_code=status.HTTP_201_CREATED)
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
    It takes the token from the URL and uses it to get the user's email address.
    The function then checks if there is a user with that email in our database,
    and if not, returns an error message. If there is such a user, we check whether
    their account has already been confirmed or not; if it has been confirmed already,
    we return another message saying so; otherwise we call repository_users' confirm_email() method.

    :param token: str: Get the token from the url
    :param db: AsyncSession: Get the database session
    :return: A message that the email has been confirmed
    :doc-author: Trelent
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirm_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_db)):
    """
    The request_email function is used to send an email to the user with a link that will allow them
    to confirm their email address. The function takes in a RequestEmail object, which contains the
    email of the user who wants to confirm their account. It then checks if there is already a confirmed
    user with that email address, and if so returns an error message saying as much. If not, it sends
    an asynchronous task (using FastAPI's BackgroundTasks) to send_email(), passing in all of the necessary information.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base url of the server
    :param db: AsyncSession: Get the database session
    :return: A dictionary with the message key and a value of check your email for confirmation
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}
