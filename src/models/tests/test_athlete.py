"""
Test Athlete class
"""
import unittest

from models.athlete import Athlete
from models.login_detail import LoginDetail


class TestAthlete(unittest.TestCase):
    """
    Test class to test Athlete
    """
    _login_details = LoginDetail(
            0,
            0,
            "refresh",
            "access"
        )
    athlete_dict = {
                "username": "username",
                "firstname": "firstname",
                "lastname": "lastname",
                "bio": "bio",
                "city": "city",
                "state": "state",
                "country": "country",
                "sex": "M",
                "created_at": "created_at",
                "updated_at": "updated_at",
                "weight": 75.2,
                "profile_medium": "profile_medium"
            }
    _test_athlete = Athlete(
        "000",
        athlete_dict,
        _login_details
    )

    def test_from_strava_auth(self):
        """Test to create an Athlete from the data returned by Strava"""
        source = {
            "athlete": {
                "username": "username",
                "firstname": "firstname",
                "lastname": "lastname",
                "bio": "bio",
                "city": "city",
                "state": "state",
                "country": "country",
                "sex": "sex",
                "created_at": "created_at",
                "updated_at": "updated_at",
                "weight": "weight",
                "profile_medium": "profile_medium"
            },
            "expires_at": "",
            "expires_in": "",
            "refresh_token": "",
            "access_token": ""
        }
        athlete = Athlete.from_strava_auth(_id=1234, source=source)

        self.assertEqual(athlete.id, "1234")  # Check that Athlete constructor works

    def test_from_db(self):
        """Test to create an Athlete from the data returned by Firebase"""
        source = {
            "username": "username",
            "firstname": "firstname",
            "lastname": "lastname",
            "bio": "bio",
            "city": "city",
            "state": "state",
            "country": "country",
            "sex": "sex",
            "created_at": "created_at",
            "updated_at": "updated_at",
            "weight": "weight",
            "profile_medium": "profile_medium",
            "login_details": {
                "expires_at": "",
                "expires_in": "",
                "refresh_token": "",
                "access_token": ""
            }
        }
        athlete = Athlete.from_db(_id=1234, source=source)
        self.assertEqual(athlete.id, "1234")  # Check that Athlete constructor works

    def test_login_details(self):
        """Test login_details property"""
        details = self._test_athlete.login_details
        self.assertEqual(details, self._login_details)

    def test_to_dict_doesnt_include_id(self):
        """Test to_dict function. Ensure the id is not returned in the dict"""
        dict_result = self._test_athlete.to_dict()
        self.assertNotIn("_id", dict_result.keys())
        self.assertNotIn("id", dict_result.keys())


if __name__ == '__main__':
    unittest.main()
