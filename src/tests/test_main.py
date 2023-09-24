"""
Test main.py functions
"""

import unittest
from typing import Dict
from unittest import mock

from fastapi.testclient import TestClient
from main import register_athlete, app

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


class MockResponse:
    """
    Mock response to a post request to Strava. Return bad data
    Mock a requests.Response object
    """
    def __init__(self, json_data: Dict, status_code: int):
        """
        Mock a requests.Response object
        """
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """
        return json data. Mock a requests.Response object
        """
        return self.json_data


# This method will be used by the mock to replace requests.post
def mocked_requests_post(*_, **__):
    """
    mock function for a post request to Strava. Return correct data
    """
    return MockResponse(TEST_PAYLOAD, 200)


def mocked_failed_requests_post(*_, **__):
    """
    mock function for a post request to Strava. Return bad data
    """
    return MockResponse({"wrong": "data"}, 400)


class TestMain(unittest.TestCase):
    """
    test main.py functions
    """
    def test_register_athlete(self):
        """
        register_athlete should return an Athlete object
        """
        athlete = register_athlete(TEST_PAYLOAD)
        self.assertEqual(athlete.id, "6833726")

    def test_ping(self):
        """
        ping to test TestClient
        """
        response = client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"msg": "pong"})

    def test_login_strava(self):
        """
        login_strava should redirect to strava OAuth
        """
        response = client.get("/login")
        redirect_url = ("https://www.strava.com/oauth/authorize?client_id=51912&response_type=code&redirect_uri=http"
                        ":%2F%2F127.0.0.1:8000%2Fexchange_token&approval_prompt=force&scope=activity:read_all")
        self.assertEqual(response.url, redirect_url)

    @mock.patch('requests.post', mocked_requests_post)
    def test_exchange_token(self):
        """
        exchange_token should return 200 if the athlete is registered
        """
        response = client.get("/exchange_token?code=abc&scope=read,activity:read_all")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"athleteId": "6833726"})

    def test_exchange_token_wrong_scope(self):
        """
        exchange_token should return error 400 if the scope is wrong
        """
        response = client.get("/exchange_token?code=abc&scope=abc")

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {"detail": "Select authorization read and activity:read_all"})

    @mock.patch('requests.post', mocked_failed_requests_post)
    def test_exchange_token_failed_post(self):
        """
        exchange_token should return error 400 if the post to Strava fail
        """
        response = client.get("/exchange_token?code=abc&scope=read,activity:read_all")

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {"detail": "Error while getting token"})


if __name__ == '__main__':
    unittest.main()
