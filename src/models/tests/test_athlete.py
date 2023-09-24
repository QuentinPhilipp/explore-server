import unittest

from src.models.Athlete import Athlete
from src.models.LoginDetail import LoginDetail


class TestAthlete(unittest.TestCase):
    
    _login_details = LoginDetail(
            0,
            0,
            "refresh",
            "access"
        )
    _test_athlete = Athlete(
        "id",
        "username",
        "firstname",
        "lastname",
        "bio",
        "city",
        "state",
        "country",
        "M",
        False,
        False,
        "2023-01-01T01:01:01Z",
        "2023-01-02T01:01:01Z",
        0,
        75.3,
        "https://image.jpg",
        login_details=_login_details
    )

    def test_from_strava_auth(self):
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
                "premium": "premium",
                "summit": "summit",
                "created_at": "created_at",
                "updated_at": "updated_at",
                "badge_type_id": "badge_type_id",
                "weight": "weight",
                "profile_medium": "profile_medium"
            },
            "expires_at": "",
            "expires_in": "",
            "refresh_token": "",
            "access_token": ""
        }
        athlete = Athlete.from_strava_auth(_id=1234, source=source)

        self.assertEqual(athlete._id, "1234")  # Check that Athlete constructor works

    def test_from_db(self):
        source = {
            "username": "username",
            "firstname": "firstname",
            "lastname": "lastname",
            "bio": "bio",
            "city": "city",
            "state": "state",
            "country": "country",
            "sex": "sex",
            "premium": "premium",
            "summit": "summit",
            "created_at": "created_at",
            "updated_at": "updated_at",
            "badge_type_id": "badge_type_id",
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
        self.assertEqual(athlete._id, "1234")  # Check that Athlete constructor works

    def test_login_details(self):
        details = self._test_athlete.login_details
        self.assertEqual(details, self._login_details)

    def test_to_dict_doesnt_include_id(self):
        dict_result = self._test_athlete.to_dict()
        self.assertNotIn("_id", dict_result.keys())
        self.assertNotIn("id", dict_result.keys())

        
if __name__ == '__main__':
    unittest.main()
