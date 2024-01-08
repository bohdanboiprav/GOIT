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
        pass

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        # self.session.select(Contact).filter_by(user=self.current_user).offset().limit().scalars.all = contacts
        # self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(current_user=self.current_user, offset=0, limit=10, db=self.session)
        self.assertEqual(result, contacts)
        # result = await get_notes(skip=0, limit=10, user=self.user, db=self.session)
        # self.assertEqual(result, notes)

    # async def test_create_note(self):
    #     body = NoteModel(title="test", description="test note", tags=[1, 2])
    #     tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
    #     self.session.query().filter().all.return_value = tags
    #     result = await create_note(body=body, user=self.user, db=self.session)
    #     self.assertEqual(result.title, body.title)
    #     self.assertEqual(result.description, body.description)
    #     self.assertEqual(result.tags, tags)
    #     self.assertTrue(hasattr(result, "id"))
