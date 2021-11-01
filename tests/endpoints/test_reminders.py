import unittest
from datetime import datetime
from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.core.settings import settings
from api.endpoints.dependencies.database import create_database_session
from api.endpoints.reminder.reminder_schemas import ReminderResponse
from api.main import app

client = TestClient(app)

AUTH_HEADER = {"Authorization": f"Bearer {settings.auth_token}"}


class TestUnauthedReminderAPI:
    def test_reminders_returns_403(self):
        url = app.url_path_for("get_reminders")
        response = client.get(url)
        assert response.status_code == 403

    def test_reminder_by_id_returns_403(self):
        url = app.url_path_for("get_reminder_by_id", reminder_id=12)
        response = client.get(url)
        assert response.status_code == 403

    def test_create_returns_403(self):
        url = app.url_path_for("create_reminders")
        response = client.post(url, data={"not": "important"})
        assert response.status_code == 403

    def test_patch_returns_403(self):
        url = app.url_path_for("edit_reminders", reminder_id=12)
        response = client.delete(url, data={"not": "important"})
        assert response.status_code == 403

    def test_delete_returns_403(self):
        url = app.url_path_for("delete_reminders", reminder_id=12)
        response = client.delete(url)
        assert response.status_code == 403


class TestEmptyDatabaseReminderAPI:
    @classmethod
    def setup_method(cls):
        def override_dependency():
            mocked_session = Mock()
            mocked_session.query().all.return_value = None
            mocked_session.query().filter_by().first.return_value = None
            return mocked_session

        app.dependency_overrides[create_database_session] = override_dependency

    @classmethod
    def teardown_method(cls):
        app.dependency_overrides = {}

    def test_list_all_returns_empty_list(self):
        url = app.url_path_for("get_reminders")
        response = client.get(url, headers=AUTH_HEADER)
        assert response.status_code == 200
        assert response.json() == []

    def test_delete_returns_404(self):
        url = app.url_path_for("delete_reminders", reminder_id=1234)
        response = client.delete(url, headers=AUTH_HEADER)
        assert response.status_code == 404


class TestReminderCreation:
    @classmethod
    def setup_method(cls):
        def override_dependency():
            mocked_session = Mock()
            mocked_session.query().filter_by().first.return_value = True
            return mocked_session

        app.dependency_overrides[create_database_session] = override_dependency

    @classmethod
    def teardown_method(cls):
        app.dependency_overrides = {}

    def test_accepts_valid_data(self):
        data = {
            "author": 2,
            "mentions": [8888],
            "content": "Test",
            "expiration": datetime.utcnow().isoformat(),
            "channel_id": 1,
            "jump_url": "https://github.com",
        }
        url = app.url_path_for("create_reminders")
        response = client.post(url, json=data, headers=AUTH_HEADER)
        assert response.status_code == 201

    def test_rejects_invalid_data(self):
        data = {
            "author_id": 1,
        }
        url = app.url_path_for("create_reminders")
        response = client.post(url, data=data, headers=AUTH_HEADER)
        assert response.status_code == 400

    class TestReminderDeletion:
        @classmethod
        def setup_method(cls):
            cls.reminder_id = 1

            def override_dependency():
                def filter_delete_reminder_id(**kwargs):
                    mock_chain = Mock()
                    if (reminder_id := kwargs.get("id")) and reminder_id == cls.reminder_id:
                        mock_chain.first.return_value = True
                    else:
                        mock_chain.first.return_value = None
                    return mock_chain

                mocked_session = Mock()
                mocked_session.query().filter_by = Mock(side_effect=filter_delete_reminder_id)

                return mocked_session

            app.dependency_overrides[create_database_session] = override_dependency

        @classmethod
        def teardown_method(cls):
            app.dependency_overrides = {}

        def test_delete_unknown_reminder_returns_404(self):
            url = app.url_path_for("delete_reminders", reminder_id=1234)
            response = client.delete(url, headers=AUTH_HEADER)
            assert response.status_code == 404

        def test_delete_known_reminder_returns_200(self):
            url = app.url_path_for("delete_reminders", reminder_id=self.reminder_id)
            response = client.delete(url, headers=AUTH_HEADER)
            assert response.status_code == 204

    class TestReminderList:
        @classmethod
        def setup_method(cls):
            cls.author_one = 1
            cls.author_two = 2

            cls.test_reminder_one = ReminderResponse(
                author_id=cls.author_one,
                active=True,
                mentions=[1],
                content="test",
                expiration=datetime.utcnow().isoformat(),
                id=1,
                channel_id=12,
                jump_url="https://github.com",
            )
            cls.test_reminder_two = ReminderResponse(
                author_id=cls.author_two,
                active=False,
                mentions=[3, 4],
                content="test2",
                expiration=datetime.utcnow().isoformat(),
                id=2,
                channel_id=123,
                jump_url="https://github.com",
            )

            def override_dependency():
                def get_reminders_filter(**kwargs):
                    mock_chain = Mock()
                    if kwargs.get("active"):
                        mock_chain.all.return_value = [cls.test_reminder_one]
                    elif (author_id := kwargs.get("author_id")) and author_id == cls.author_two:
                        mock_chain.all.return_value = [cls.test_reminder_two]

                    return mock_chain

                mocked_session = Mock()
                mocked_session.query().all.return_value = [cls.test_reminder_one, cls.test_reminder_two]
                mocked_session.query().filter_by = Mock(side_effect=get_reminders_filter)
                return mocked_session

            app.dependency_overrides[create_database_session] = override_dependency

        @classmethod
        def teardown_method(cls):
            app.dependency_overrides = {}

        def test_reminders_in_full_list(self):
            url = app.url_path_for("get_reminders")
            response = client.get(url, headers=AUTH_HEADER)
            assert response.status_code == 200
            case = unittest.TestCase()
            case.assertCountEqual(response.json(), [self.test_reminder_one.dict(), self.test_reminder_two.dict()])

        def test_filter_by_active_field(self):
            url = app.url_path_for("get_reminders")
            response = client.get(url, headers=AUTH_HEADER, params={"active": True})
            assert response.status_code == 200
            assert response.json() == [self.test_reminder_one]

        def test_filter_by_author_field(self):
            url = app.url_path_for("get_reminders")
            response = client.get(url, headers=AUTH_HEADER, params={"author__id": 2})
            assert response.status_code == 200
            assert response.json() == [self.test_reminder_two]

    class TestReminderRetrieve:
        @classmethod
        def setup_method(cls):
            cls.reminder_id = 1
            cls.test_reminder = ReminderResponse(
                author_id=1,
                active=True,
                mentions=[1],
                content="test",
                expiration=datetime.utcnow().isoformat(),
                id=1,
                channel_id=12,
                jump_url="https://github.com",
            )

            def override_dependency():
                def filter_retrieve_by_reminder_id(**kwargs):
                    mock_chain = Mock()
                    if (reminder_id := kwargs.get("id")) and reminder_id == cls.reminder_id:
                        mock_chain.first.return_value = cls.test_reminder
                    else:
                        mock_chain.first.return_value = None
                    return mock_chain

                mocked_session = Mock()
                mocked_session.query().filter_by = Mock(side_effect=filter_retrieve_by_reminder_id)

                return mocked_session

            app.dependency_overrides[create_database_session] = override_dependency

        @classmethod
        def teardown_method(cls):
            app.dependency_overrides = {}

        def test_retrieve_unknown_returns_404(self):
            url = app.url_path_for("get_reminder_by_id", reminder_id=1234)
            response = client.get(url, headers=AUTH_HEADER)
            assert response.status_code == 404

        def test_retrieve_known_returns_200(self):
            url = app.url_path_for("get_reminder_by_id", reminder_id=self.reminder_id)
            response = client.get(url, headers=AUTH_HEADER)
            assert response.status_code == 200

    class TestReminderUpdate:
        @classmethod
        def setup_method(cls):
            cls.reminder_id = 1

            def override_dependency():
                mocked_session = Mock()
                mocked_session.query().filter_by().first.return_value = True
                return mocked_session

            app.dependency_overrides[create_database_session] = override_dependency

        @classmethod
        def teardown_method(cls):
            app.dependency_overrides = {}

        def test_patch_updates_record(self):
            url = app.url_path_for("get_reminder_by_id", reminder_id=self.reminder_id)
            response = client.patch(url, headers=AUTH_HEADER, json={"content": "Oops I forgot"})
            assert response.status_code == 200
