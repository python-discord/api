from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.core.database.models.api.bot import OffTopicChannelName
from api.core.settings import settings
from api.endpoints.dependencies.database import create_database_session
from api.main import app

client = TestClient(app)

AUTH_HEADER = {"Authorization": f"Bearer {settings.auth_token}"}


class TestUnauthenticated:
    def test_cannot_read_off_topic_channel_name_list(self):
        """Return a 401 response when not authenticated."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(url)

        assert response.status_code == 403

    def test_cannot_read_off_topic_channel_name_list_with_random_item_param(self):
        """Return a 401 response when `random_items` provided and not authenticated."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(f"{url}?random_items=no")

        assert response.status_code == 403


class TestEmptyDatabase:
    @classmethod
    def setup_method(cls):
        def override_dependency():
            mocked_session = Mock()
            mocked_session.query().all.return_value = []
            return mocked_session

        app.dependency_overrides[create_database_session] = override_dependency

    @classmethod
    def teardown_method(cls):
        app.dependency_overrides = {}

    def test_returns_empty_object(self):
        """Return empty list when no names in database."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(url, headers=AUTH_HEADER)

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_empty_list_with_get_all_param(self):
        """Return empty list when no names and `random_items` param provided."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(f"{url}?random_items=5", headers=AUTH_HEADER)

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_400_for_bad_random_items_param(self):
        """Return error message when passing not integer as `random_items`."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(
            f"{url}?random_items=totally-a-valid-integer", headers=AUTH_HEADER
        )

        assert response.status_code == 400
        assert response.json(), {
            "error": [
                {
                    "loc": ["query", "random_items"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }

    def test_returns_400_for_negative_random_items_param(self):
        """Return error message when passing negative int as `random_items`."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(f"{url}?random_items=-5", headers=AUTH_HEADER)

        assert response.status_code == 404
        assert response.json(), {
            "error": ["'random_items' must be a positive integer."]
        }


class TestListView:
    @classmethod
    def setup_method(cls):
        cls.test_name = OffTopicChannelName(name="lemons-lemonade-stand", used=True)
        cls.test_name_2 = OffTopicChannelName(name="bbq-with-bisk", used=True)

        def override_dependency():
            mocked_session = Mock()
            mocked_session.query().all().order_by.return_value = [
                cls.test_name,
                cls.test_name_2,
            ]
            mocked_session.query().all.return_value = [cls.test_name, cls.test_name_2]

            return mocked_session

        app.dependency_overrides[create_database_session] = override_dependency

    @classmethod
    def teardown_method(cls):
        app.dependency_overrides = {}

    def test_returns_name_in_list(self):
        """Return all off-topic channel names."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(url, headers=AUTH_HEADER)

        assert response.status_code == 200
        assert response.json(), [self.test_name.name, self.test_name_2.name]

    def test_returns_single_item_with_random_items_param_set_to_1(self):
        """Return not-used name instead used."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(f"{url}?random_items=1", headers=AUTH_HEADER)

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json(), [self.test_name.name]

    def test_running_out_of_names_with_random_parameter(self):
        """Reset names `used` parameter to `False` when running out of names."""
        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(f"{url}?random_items=2", headers=AUTH_HEADER)

        assert response.status_code == 200
        assert response.json(), [self.test_name.name, self.test_name_2.name]


class TestCreationView:
    @classmethod
    def setup_method(cls):
        def override_dependency():
            mocked_session = Mock()
            return mocked_session

        app.dependency_overrides[create_database_session] = override_dependency

    @classmethod
    def teardown_method(cls):
        app.dependency_overrides = {}

    def test_returns_201_for_unicode_chars(self):
        """Accept all valid characters."""
        url = app.url_path_for("create_off_topic_channel_names")
        names = (
            "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹",
            "ǃ？’",
        )

        for name in names:
            response = client.post(f"{url}?name={name}", headers=AUTH_HEADER)
            assert response.status_code == 201

    def test_returns_400_for_missing_name_param(self):
        """Return error message when name not provided."""
        url = app.url_path_for("create_off_topic_channel_names")
        response = client.post(url, headers=AUTH_HEADER)

        assert response.status_code == 400
        assert response.json(), {
            "error": [
                {
                    "loc": ["query", "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }

    def test_returns_400_for_bad_name_param(self):
        """Return error message when invalid characters provided."""
        url = app.url_path_for("create_off_topic_channel_names")
        invalid_names = (
            "space between words",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "!?'@#$%^&*()",
        )

        for name in invalid_names:
            response = client.post(f"{url}?name={name}", headers=AUTH_HEADER)
            assert response.status_code == 400
            assert response.json(), {
                "error": f"{name} is not a valid Off Topic channel name!"
            }


class TestDeletionView:
    @classmethod
    def setup_method(cls):
        cls.test_name = "lemons-lemonade-stand"
        cls.test_name_2 = "bbq-with-bisk"

        def override_dependency():
            def filter_delete_otn_name(**kwargs):
                mock_chain = Mock()
                if kwargs.get("name") in (cls.test_name, cls.test_name_2):
                    mock_chain.first.return_value = True
                else:
                    mock_chain.first.return_value = None
                return mock_chain

            mocked_session = Mock()
            mocked_session.query().all.return_value = []
            mocked_session.query().filter_by = Mock(side_effect=filter_delete_otn_name)

            return mocked_session

        app.dependency_overrides[create_database_session] = override_dependency

    @classmethod
    def teardown_method(cls):
        app.dependency_overrides = {}

    def test_deleting_unknown_name_returns_404(self):
        """Return 404 response when trying to delete unknown name."""
        url = app.url_path_for("delete_off_topic_channel_names")
        response = client.delete(f"{url}?name=unknown-name", headers=AUTH_HEADER)

        assert response.status_code == 404

    def test_deleting_known_name_returns_204(self):
        """Return 204 response when deleting was successful."""
        url = app.url_path_for("delete_off_topic_channel_names")
        response = client.delete(f"{url}?name={self.test_name}", headers=AUTH_HEADER)

        assert response.status_code == 204

    def test_name_gets_deleted(self):
        """Name gets actually deleted."""
        url = app.url_path_for("delete_off_topic_channel_names")
        response = client.delete(f"{url}?name={self.test_name_2}", headers=AUTH_HEADER)
        assert response.status_code == 204

        url = app.url_path_for("get_off_topic_channel_names")
        response = client.get(url, headers=AUTH_HEADER)
        assert self.test_name_2 not in response.json()
