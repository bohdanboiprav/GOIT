import datetime

from faker import Faker
import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.contact import ContactModel

fake = Faker()


async def populate_contacts(count: int, current_user: User, db: AsyncSession):
    """
    The populate_contacts function is used to populate the database with fake contacts.
    It takes in a count parameter, which specifies how many contacts should be created.
    The current_user parameter is used to specify the user who will own these new contacts.
    Finally, db is an async session object that allows us to interact with our database.

    :param count: int: Specify the number of contacts to be created
    :param current_user: User: Get the current user
    :param db: AsyncSession: Pass the database session to the function
    :return: A string
    :doc-author: Trelent
    """
    for _ in range(count):
        contact = Contact(name=fake.first_name(), surname=fake.last_name(), email=fake.email(),
                          phone=fake.phone_number(), date_of_birth=fake.date_of_birth(),
                          additional_info=fake.text() if random.randint(0, 1) == 1 else None, user=current_user)
        db.add(contact)
    await db.commit()
    return "Contacts populated"


async def get_contacts(current_user: User, limit: int, offset: int, db: AsyncSession):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param current_user: User: Filter the contacts by user
    :param limit: int: Limit the number of contacts returned from the database
    :param offset: int: Specify the number of records to skip before returning the results
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = select(Contact).filter_by(user=current_user).offset(offset).limit(limit)
    contacts = await db.execute(contacts)
    return contacts.scalars().all()


async def get_contacts_by(name: str, surname: str, email: str, current_user: User, db: AsyncSession):
    """
    The get_contacts_by function returns a list of contacts that match the given parameters.
    If no parameter is provided, all contacts are returned.

    :param name: str: Filter the contacts by name
    :param surname: str: Filter the contacts by surname
    :param email: str: Filter the contacts by email
    :param current_user: User: Get the current user from the database
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = select(Contact).filter_by(user=current_user)
    if name:
        contacts = contacts.filter(Contact.name == name)
    if surname:
        contacts = contacts.filter(Contact.surname == surname)
    if email:
        contacts = contacts.filter(Contact.email == email)
    contacts = await db.execute(contacts)
    return contacts.scalars().all()


async def get_contacts_birthdays(current_user: User, db: AsyncSession):
    """
    The get_contacts_birthdays function returns a list of contacts whose birthdays are within the next 7 days.
    The function takes in two arguments: current_user and db. The current_user argument is an instance of the User
    class,and it represents the user who is currently logged into their account on our application. The db argument is
    an instance of AsyncSession, which allows us to execute SQLAlchemy queries asynchronously.

    :param current_user: User: Get the current user from the database
    :param db: AsyncSession: Get the database session
    :return: A list of contacts that have birthdays in the next seven days
    :doc-author: Trelent
    """
    today = datetime.date.today()
    seven_days_later = today + datetime.timedelta(days=7)
    contacts = select(Contact).filter_by(user=current_user)
    return_data = []
    contacts = await db.execute(contacts)
    for contact in contacts.scalars().all():
        birthday = contact.date_of_birth
        birthday = birthday.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        if today <= birthday <= seven_days_later:
            return_data.append(contact)
    return return_data


async def get_contact(contact_id: int, current_user: User, db: AsyncSession):
    """
    The get_contact function is used to retrieve a single contact from the database.
    It takes in three arguments:
        - contact_id: The id of the contact you want to retrieve. This is an integer value.
        - current_user: The user who wants to get this specific contact, which will be passed in by FastAPI's dependency
        injection system (see below). This is a User object that contains information about the currently logged-in
        user, such as their username and password hash. It also has an id attribute that can be used for querying
        contacts associated with this particular user (i.e., only return contacts where Contact

    :param contact_id: int: Filter the contact by id
    :param current_user: User: Check that the user is logged in
    :param db: AsyncSession: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = select(Contact).filter_by(user=current_user).filter(Contact.id == contact_id)
    contact = await db.execute(contact)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactModel, current_user: User, db: AsyncSession):
    """
    The create_contact function creates a new contact in the database.
        Args:
            body (ContactModel): The contact to create.
            current_user (User): The user who is creating the contact.
            db (AsyncSession): A database session for making queries and commits.

    :param body: ContactModel: Get the data from the request body
    :param current_user: User: Get the user who is currently logged in
    :param db: AsyncSession: Pass the database session to the function
    :return: The contact object that was created
    :doc-author: Trelent
    """
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone,
                      date_of_birth=body.date_of_birth, additional_info=body.additional_info, user=current_user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, current_user: User, db: AsyncSession):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified user's contact.
                This is passed as JSON in the request body and deserialized into this model by Pydantic.
                See models/contact_model for more details on what fields are required and their types, etc...

    :param contact_id: int: Specify the contact id of the contact that is going to be deleted
    :param body: ContactModel: Get the data from the request body
    :param current_user: User: Get the user who is currently logged in
    :param db: AsyncSession: Pass the database session to the function
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = select(Contact).filter_by(user=current_user).filter(Contact.id == contact_id)
    result = await db.execute(contact)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.date_of_birth = body.date_of_birth
        contact.additional_info = body.additional_info
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, current_user: User, db: AsyncSession):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the id of the contact to be removed
    :param current_user: User: Ensure that the user is logged in and has access to their contacts
    :param db: AsyncSession: Pass the database session to the function
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    contact = select(Contact).filter_by(user=current_user).filter(Contact.id == contact_id)
    result = await db.execute(contact)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
