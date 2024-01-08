import unittest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas.user import UserModel
from src.repository.users import get_user_by_email, create_user, update_token, confirm_email, update_avatar


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.current_user = User(id=1, username="test", email="example@example.com", password="password")
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_user_by_email(self):
        user = User()
        mocked_user = MagicMock()
        mocked_user.scalars.return_value.first.return_value = user
        self.session.execute.return_value = mocked_user
        result = await get_user_by_email('example@example.com', self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        body = UserModel(username='Test',
                         email='test@test.com', password='066221111')
        result = await create_user(body, self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.email, body.email)

    async def test_update_token(self):
        user = User()
        refresh_token = 'refresh_token'
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = User()
        self.session.execute.return_value = mocked_user
        upd_result = await update_token(user, refresh_token, self.session)
        self.assertEqual(upd_result, None)

    async def test_confirm_email(self):
        email = 'test@test.com'
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = User()
        self.session.execute.return_value = mocked_user
        upd_result = await confirm_email(email, self.session)
        self.assertEqual(upd_result, None)

    async def test_update_avatar(self):
        email = 'test@test.com'
        link = 'https://www.google.com/'
        mocked_user = MagicMock()
        mocked_user.scalars.return_value.first.return_value = User()
        self.session.execute.return_value = mocked_user
        upd_result = await update_avatar(email, link, self.session)
        self.assertIsInstance(upd_result, User)
