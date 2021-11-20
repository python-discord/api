from datetime import datetime
from operator import itemgetter

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database.models.api.bot import Reminder, User
from api.endpoints.reminder.reminder_schemas import ReminderResponse

pytestmark = pytest.mark.asyncio


class TestUnauthedReminderAPI:

    @pytest.fixture()
    def yield_self(self):
        yield self

    @pytest.fixture(autouse=True)
    async def inject_config_unauthed_reminder(self, unauthed_client, app, yield_self):
        yield_self.client = unauthed_client
        yield_self.app = app

    async def test_reminders_returns_403(self):
        url = self.app.url_path_for("get_reminders")
        response = await self.client.get(url)
        assert response.status_code == 403

    async def test_reminder_by_id_returns_403(self):
        url = self.app.url_path_for("get_reminder_by_id", reminder_id=12)
        response = await self.client.get(url)
        assert response.status_code == 403

    async def test_create_returns_403(self):
        url = self.app.url_path_for("create_reminders")
        response = await self.client.post(url, json={"not": "important"})
        assert response.status_code == 403

    async def test_patch_returns_403(self):
        url = self.app.url_path_for("edit_reminders", reminder_id=12)
        response = await self.client.patch(url, json={"not": "important"})
        assert response.status_code == 403

    async def test_delete_returns_403(self):
        url = self.app.url_path_for("delete_reminders", reminder_id=12)
        response = await self.client.delete(url)
        assert response.status_code == 403


class TestEmptyDatabaseReminderAPI:
    @pytest.fixture()
    def yield_self(self):
        yield self

    @pytest.fixture(autouse=True)
    async def inject_config_empty_db(self, client, app, yield_self):
        yield_self.client = client
        yield_self.app = app

    async def test_list_all_returns_empty_list(self):
        url = self.app.url_path_for("get_reminders")
        response = await self.client.get(url)
        assert response.status_code == 200
        assert response.json() == []

    async def test_delete_returns_404(self):
        url = self.app.url_path_for("delete_reminders", reminder_id=1234)
        response = await self.client.delete(url)
        assert response.status_code == 404


class TestReminderCreation:
    @pytest.fixture()
    def yield_self(self):
        yield self

    @pytest.fixture(autouse=True)
    async def inject_config_reminder_creation_eizo(self, async_db_session, client, app, yield_self):
        yield_self.client = client
        yield_self.app = app
        test_user = User(name="test_user", discriminator=1212)
        async_db_session.add(test_user)
        await async_db_session.commit()
        await async_db_session.refresh(test_user)
        yield_self.test_user = test_user

    async def test_accepts_valid_data(self, async_db_session):
        data = {
            "author": self.test_user.id,
            "mentions": [8888],
            "content": "Test",
            "expiration": datetime.utcnow().isoformat(),
            "channel_id": 1,
            "jump_url": "https://github.com",
        }
        url = self.app.url_path_for("create_reminders")
        response = await self.client.post(url, json=data)
        await async_db_session.commit()
        assert (await async_db_session.execute(select(Reminder))).scalars().first()
        assert response.status_code == 201

    async def test_rejects_invalid_data(self, async_db_session):
        data = {
            "author_id": 1,
        }
        url = self.app.url_path_for("create_reminders")
        response = await self.client.post(url, json=data)
        assert response.status_code == 400
        assert not (await async_db_session.execute(select(Reminder))).scalars().first()

    class TestReminderDeletion:
        @pytest.fixture()
        def yield_self(self):
            yield self

        @pytest.fixture(scope="function", autouse=True)
        async def inject_config_reminder_deletion(self, async_db_session, yield_self, client,
                                                  app):
            yield_self.app = app
            yield_self.client = client
            test_user = User(name="test_user", discriminator=1212)
            test_reminder = Reminder(
                channel_id=1,
                content="test",
                expiration=datetime.now(),
                author=test_user,
                jump_url="https://github.com",
                mentions=[1]
            )
            async_db_session.add(test_user)
            async_db_session.add(test_reminder)
            await async_db_session.commit()
            await async_db_session.refresh(test_reminder)

            yield_self.test_reminder = test_reminder

        async def test_delete_unknown_reminder_returns_404(self):
            url = self.app.url_path_for("delete_reminders", reminder_id=1234)
            response = await self.client.delete(url)
            assert response.status_code == 404

        async def test_delete_known_reminder_returns_200(self, async_db_session):
            url = self.app.url_path_for("delete_reminders", reminder_id=self.test_reminder.id)
            response = await self.client.delete(url)
            await async_db_session.commit()
            assert response.status_code == 204
            assert not (await async_db_session.execute(
                select(Reminder).where(Reminder.id == self.test_reminder.id))).scalars().first()

    class TestReminderList:
        @pytest.fixture()
        def yield_self(self):
            yield self

        @pytest.fixture(scope="function", autouse=True)
        async def inject_config_reminder_list(self, async_db_session, yield_self, client, app):
            yield_self.client = client
            yield_self.app = app
            test_user_first = User(name="test_user", discriminator=1212)
            test_user_second = User(name="test_user2", discriminator=1212)
            test_reminder_one = Reminder(
                active=False,
                channel_id=1,
                content="test",
                expiration=datetime.now(),
                author=test_user_first,
                jump_url="https://github.com"
            )
            test_reminder_two = Reminder(
                channel_id=1,
                content="test2",
                expiration=datetime.now(),
                author=test_user_second,
                jump_url="https://github.com"
            )

            async_db_session.add_all([test_user_first, test_user_second, test_reminder_one, test_reminder_two])
            await async_db_session.commit()
            await async_db_session.refresh(test_reminder_one)
            await async_db_session.refresh(test_reminder_two)
            yield_self.test_reminder_one = ReminderResponse.from_orm(test_reminder_one).dict()
            yield_self.test_reminder_two = ReminderResponse.from_orm(test_reminder_two).dict()

        async def test_reminders_in_full_list(self):
            url = self.app.url_path_for("get_reminders")
            response = await self.client.get(url, )
            assert response.status_code == 200
            assert sorted(response.json(), key=itemgetter("id")) == sorted(
                [self.test_reminder_one, self.test_reminder_two],
                key=itemgetter("id"),
            )

        async def test_filter_by_active_field(self):
            url = self.app.url_path_for("get_reminders")
            response = await self.client.get(url, params={"active": True})
            assert response.status_code == 200
            assert response.json() == [self.test_reminder_two]

        async def test_filter_by_author_field(self):
            url = self.app.url_path_for("get_reminders")
            response = await self.client.get(url, params={"author__id": self.test_reminder_one["author"]})
            assert response.status_code == 200
            assert response.json() == [self.test_reminder_one]

    class TestReminderRetrieve:

        @pytest.fixture()
        def yield_self(self):
            yield self

        @pytest.fixture(scope="function", autouse=True)
        async def inject_config_reminder_retrieve(self, async_db_session, client, app, yield_self):
            yield_self.app = app
            yield_self.client = client

            test_user = User(name="test_user", discriminator=1212)
            test_reminder = Reminder(
                channel_id=1,
                content="test",
                expiration=datetime.now(),
                author=test_user,
                jump_url="https://github.com"
            )
            async_db_session.add(test_user)
            async_db_session.add(test_reminder)
            await async_db_session.commit()
            await async_db_session.refresh(test_reminder)

            yield_self.test_reminder = test_reminder

        async def test_retrieve_unknown_returns_404(self):
            url = self.app.url_path_for("get_reminder_by_id", reminder_id=1234)
            response = await self.client.get(url)
            assert response.status_code == 404

        async def test_retrieve_known_returns_200(self):
            url = self.app.url_path_for("get_reminder_by_id", reminder_id=self.test_reminder.id)
            response = await self.client.get(url)
            assert response.status_code == 200

    class TestReminderUpdate:

        @pytest.fixture()
        def yield_self(self):
            yield self

        @pytest.fixture(scope="function", autouse=True)
        async def inject_config_reminder_update(self, async_db_session: AsyncSession, client, app, yield_self):
            yield_self.app = app
            yield_self.client = client
            test_user = User(name="test_user", discriminator=1212)
            test_reminder = Reminder(
                channel_id=1,
                content="test",
                expiration=datetime.now(),
                author=test_user,
                jump_url="https://github.com",
                mentions=[1]
            )
            async_db_session.add(test_user)
            async_db_session.add(test_reminder)
            await async_db_session.commit()
            await async_db_session.refresh(test_reminder)
            yield_self.test_data = {"content": "Oops I forgot"}
            yield_self.test_reminder = test_reminder

        async def test_patch_updates_record(self, async_db_session: AsyncSession):
            url = self.app.url_path_for("edit_reminders", reminder_id=self.test_reminder.id)
            response = await self.client.patch(url, json=self.test_data)
            await async_db_session.commit()
            assert response.status_code == 200
            assert (await async_db_session.execute(
                select(Reminder).filter_by(id=self.test_reminder.id)
            )).scalars().first().content == self.test_data["content"]
