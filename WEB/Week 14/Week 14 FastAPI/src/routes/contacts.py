from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas.contact import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=2, le=500), offset: int = Query(0, ge=0),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: AsyncSession = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts for the current user.
    The limit and offset parameters are used to paginate the results.


    :param limit: int: Limit the number of contacts returned
    :param ge: Set the minimum value for the limit parameter
    :param le: Limit the number of contacts returned
    :param offset: int: Skip a number of records from the beginning
    :param ge: Specify that the limit must be greater than or equal to 2
    :param current_user: User: Get the current user from the database
    :param db: AsyncSession: Get the database session
    :return: A list of contacts
    :doc-author: Trelent
    """
    return await repository_contacts.get_contacts(current_user, limit, offset, db)


@router.get("/by", response_model=list[ContactResponse])
async def get_contacts_by(name: str = Query(None, min_length=1, max_length=70),
                          surname: str = Query(None, min_length=1, max_length=70),
                          email: str = Query(None, min_length=1, max_length=70),
                          current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    """
    The get_contacts_by function is used to retrieve contacts from the database.
    The function takes in a name, surname and email as parameters. The current_user parameter is used to get the user's
    id from the token that was passed in with the request header. The db parameter is used to create an async session
    with the database so that queries can be made against it.

    :param name: str: Filter the contacts by name
    :param min_length: Specify the minimum length of a string
    :param max_length: Check the length of the string
    :param surname: str: Filter the contacts by surname
    :param min_length: Set the minimum length of a string
    :param max_length: Limit the length of the string
    :param email: str: Search for contacts by email
    :param min_length: Set the minimum length of the parameter
    :param max_length: Limit the length of a string
    :param current_user: User: Get the current user from the database
    :param db: AsyncSession: Pass the database session to the repository
    :return: A list of contacts
    :doc-author: Trelent
    """
    return await repository_contacts.get_contacts_by(name, surname, email, current_user, db)


@router.get("/birthdays", response_model=list[ContactResponse])
async def get_contacts_by(current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    """
    The get_contacts_by function returns a list of contacts that have birthdays in the current month.
        The function takes two parameters:
            - current_user: A User object representing the user making the request. This is passed by default to all
            endpoints, and can be accessed using Depends(auth_service.get_current_user).
            - db: An AsyncSession object representing an open database connection, which is passed by default to all
            endpoints, and can be accessed using Depends(get_db).

    :param current_user: User: Get the current user
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    return await repository_contacts.get_contacts_birthdays(current_user, db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user),
                      db: AsyncSession = Depends(get_db)):
    """
    The get_contact function returns a contact by its id.

    :param contact_id: int: Specify that the contact_id parameter is an integer
    :param current_user: User: Get the current user from the database
    :param db: AsyncSession: Get the database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.post("/create", response_model=ContactResponse, description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user),
                         db: AsyncSession = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param current_user: User: Get the user that is currently logged in
    :param db: AsyncSession: Pass the database session to the repository
    :return: A contactmodel object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.post("/populate/{count}", description='No more than 1 requests per minute',
             dependencies=[Depends(RateLimiter(times=1, seconds=60))])
async def populate_contact(count: int = Path(ge=1, le=150), current_user: User = Depends(auth_service.get_current_user),
                           db: AsyncSession = Depends(get_db)):
    """
    The populate_contact function is used to populate the database with a number of contacts.
    The function takes in an integer count, which represents the number of contacts to be created.
    The function also takes in a current_user object and db session object as dependencies.

    :param count: int: Specify the number of contacts to create
    :param le: Limit the number of contacts that can be created at once
    :param current_user: User: Get the current user from the database
    :param db: AsyncSession: Get a database session
    :return: A list of contacts
    :doc-author: Trelent
    """
    return await repository_contacts.populate_contacts(count, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1),
                         current_user: User = Depends(auth_service.get_current_user),
                         db: AsyncSession = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id of the contact to update, and a body containing
        all fields that should be updated.

    :param body: ContactModel: Validate the request body
    :param contact_id: int: Get the contact id from the url path
    :param current_user: User: Get the current user from the auth_service
    :param db: AsyncSession: Get the database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact id that is passed in the url
    :param db: AsyncSession: Get the database session
    :param current_user: User: Get the current user from the request
    :return: The removed contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact
