import unittest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.contact import ContactModel
from src.repository.contacts import (populate_contacts, get_contacts, get_contacts_by, get_contacts_birthdays,
                                     get_contact, create_contact, update_contact, remove_contact)


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.current_user = User(id=1, username="test", email="example@example.com", password="password")
        self.session = AsyncMock(spec=AsyncSession)

    async def test_populate_contacts(self):
        result = await populate_contacts(count=10, current_user=self.current_user, db=self.session)
        self.assertEqual(result, "Contacts populated")

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(current_user=self.current_user, offset=0, limit=10, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by(self):
        contacts = [Contact(), Contact(), Contact()]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts_by(name='Test', surname='Test', email='test@example.com',
                                       current_user=self.current_user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact()
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(contact_id=1, current_user=self.current_user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contacts_birthdays(self):
        contacts = []
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts_birthdays(current_user=self.current_user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactModel(name='TestU', surname='Test',
                            email='test@test.com', phone='066221111',
                            date_of_birth='2004-01-08', additional_info='string')
        result = await create_contact(body, self.current_user, self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertEqual(result.additional_info, body.additional_info)

    async def test_update_contact(self):
        body = ContactModel(name='TestUpd', surname='TestUpd',
                            email='test@test.com', phone='066221111',
                            date_of_birth='2004-01-08', additional_info='string')
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact()
        self.session.execute.return_value = mocked_contact
        upd_result = await update_contact(1, body, self.current_user, self.session)
        self.assertIsInstance(upd_result, Contact)
        self.assertEqual(upd_result.name, body.name)
        self.assertEqual(upd_result.surname, body.surname)
        self.assertEqual(upd_result.email, body.email)
        self.assertEqual(upd_result.phone, body.phone)
        self.assertEqual(upd_result.date_of_birth, body.date_of_birth)
        self.assertEqual(upd_result.additional_info, body.additional_info)

    async def test_remove_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact()
        self.session.execute.return_value = mocked_contact
        result = await remove_contact(1, self.current_user, self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result, mocked_contact.scalar_one_or_none.return_value)
