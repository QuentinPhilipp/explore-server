import unittest

from fastapi.testclient import TestClient
from src.main import register_athlete, app
from unittest import mock

client = TestClient(app)

TEST_PAYLOAD = \
    {
        'token_type': 'Bearer', 'expires_at': 1695474236, 'expires_in': 18247,
        'refresh_token': '96b5fd88695ea2fa7897ad195d9eea4b42f333a7',
        'access_token': '52c249fb9b21c2f0fb87c08c26419de278d1edf6',
        'athlete': {
            'id': 6833726, 'username': 'quentinphilipp',
            'resource_state': 2, 'firstname': 'Quentin',
            'lastname': 'Philipp', 'bio': '', 'city': 'Lemberg',
            'state': 'Moselle', 'country': 'France', 'sex': 'M',
            'premium': False, 'summit': False, 'created_at': '2014-10-19T22:44:26Z',
            'updated_at': '2023-09-13T19:38:47Z', 'badge_type_id': 0,
            'weight': 80.0,
            'profile_medium': 'https://graph.facebook.com/1012000325614886/picture?height=256&width=256',
            'profile': 'https://graph.facebook.com/1012000325614886/picture?height=256&width=256',
            'friend': None,
            'follower': None
        }
    }


# This method will be used by the mock to replace requests.post
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(TEST_PAYLOAD, 200)


def mocked_failed_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse({"wrong": "data"}, 400)


class TestMain(unittest.TestCase):
    def test_register_athlete(self):
        athlete = register_athlete(TEST_PAYLOAD)
        self.assertEqual(athlete.id, "6833726")

    def test_ping(self):
        response = client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"msg": "pong"})

    def test_login_strava(self):
        response = client.get("/login")
        redirect_url = ("https://www.strava.com/oauth/authorize?client_id=51912&response_type=code&redirect_uri=http"
                        ":%2F%2F127.0.0.1:8000%2Fexchange_token&approval_prompt=force&scope=activity:read_all")
        self.assertEqual(response.url, redirect_url)

    @mock.patch('requests.post', mocked_requests_post)
    def test_exchange_token(self):
        response = client.get("/exchange_token?code=abc&scope=read,activity:read_all")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"athleteId": "6833726"})

    def test_exchange_token_wrong_scope(self):
        response = client.get("/exchange_token?code=abc&scope=abc")

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {"detail": "Select authorization read and activity:read_all"})

    @mock.patch('requests.post', mocked_failed_requests_post)
    def test_exchange_token_failed_post(self):
        response = client.get("/exchange_token?code=abc&scope=read,activity:read_all")

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {"detail": "Error registering athlete. 'athlete'"})


if __name__ == '__main__':
    unittest.main()
