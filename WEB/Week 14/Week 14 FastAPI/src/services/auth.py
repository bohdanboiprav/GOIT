import pickle
from typing import Optional

import redis
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import settings
from src.database.db import get_db
from src.repository import users as repository_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
        The hash is generated using the pwd_context object, which is an instance of Bcrypt's Bcrypt class.

        :param self: Represent the instance of the class
        :param password: str: Specify the password that will be hashed
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        """
        The verify_password function takes a plain-text password and a hashed password,
        and returns True if the passwords match. It uses the same hash function as generate_password_hash.

        :param self: Represent the instance of the class
        :param plain_password: str: Pass in the password that is being verified
        :param hashed_password: str: Pass the hashed password from the database
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token.
            Args:
                data (dict): A dictionary containing the claims to be encoded in the JWT.
                expires_delta (Optional[float]): An optional parameter specifying how long, in seconds,
                    the access token should last before expiring. If not specified, it defaults to 15 minutes.

        :param self: Refer to the current instance of a class
        :param data: dict: Pass the data that will be encoded in the jwt
        :param expires_delta: Optional[float]: Set the expiration time of the access token
        :return: A string
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): A dictionary containing the user's id and username.
                expires_delta (Optional[float]): The number of seconds until the token expires, defaults to None.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the user's data
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: An encoded refresh token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def create_email_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_email_token function takes in a dictionary of data, and an optional expires_delta parameter.
        The function then creates a token that will expire after the specified time period (expires_delta).
        If no expires_delta is provided, the token will expire after 15 days. The function returns an encoded email
        token.

        :param self: Access the class attributes
        :param data: dict: Pass the data that will be encoded in the token
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: A token, which is a string
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        encoded_email_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_email_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function decodes the refresh token and returns the email of the user.
        If it fails to decode, it raises an HTTPException with a 401 status code and detail message.

        :param self: Represent the instance of a class
        :param refresh_token: str: Pass in the refresh token that is sent to the server
        :return: The email address of the user that is associated with the refresh token
        :doc-author: Trelent
        """
        try:
            decoded_refresh_token = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if decoded_refresh_token["scope"] == "refresh_token":
                email = decoded_refresh_token["sub"]
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email associated with that token.
        It does this by decoding the token using jwt.decode, which is part of PyJWT, a Python library for encoding and
        decoding JSON Web Tokens (JWTs).
        The decode function takes three arguments: the JWT to be decoded; our SECRET_KEY; and our ALGORITHM (HS256).
        If successful, it will return a dictionary containing information about the JWT's payload.
        We check that this payload has scope &quot;email_token&quot; before returning its sub field.

        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :return: The email of the user who is trying to verify their account
        :doc-author: Trelent
        """
        try:
            decoded_email_token = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if decoded_email_token["scope"] == "email_token":
                email = decoded_email_token["sub"]
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token for email verification')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the
            protected endpoints. It takes a token as an argument and returns the user
            if it's valid, or raises an exception otherwise.

        :param self: Access the class attributes
        :param token: str: Get the token from the authorization header
        :param db: AsyncSession: Get the database session
        :return: A user object
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user_hash = str(email)
        user = self.r.get(user_hash)
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(user_hash, pickle.dumps(user))
            self.r.expire(user_hash, 300)
        else:
            print("User from cache")
            user = pickle.loads(user)
        return user


auth_service = Auth()
