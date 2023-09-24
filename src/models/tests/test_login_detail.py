"""
Test Athlete class
"""
import unittest

from models.login_detail import LoginDetail


class TestLoginDetail(unittest.TestCase):
    """
    Test class to test LoginDetail
    """
    _login_details = LoginDetail(
        1672560000,
        1234,
        "refresh_token_abcdefghij123456789",
        "access_token_abcdefghij123456789"
    )

    def test_from_db(self):
        """Test to create an LoginDetail from the data returned by Firebase"""
        source = {
            "expires_at": 1672560000,
            "expires_in": 1234,
            "refresh_token": "refresh_token_abcdefghij123456789",
            "access_token": "access_token_abcdefghij123456789"
        }
        login_info = LoginDetail.from_db(source=source)
        # Check that LoginDetails constructor works
        self.assertEqual(login_info.refresh_token, "refresh_token_abcdefghij123456789")

    def test_to_dict(self):
        """Test to export a LoginDetail to dict"""
        login_dict = self._login_details.to_dict()
        expected_data = {
            "expires_at": 1672560000,
            "expires_in": 1234,
            "refresh_token": "refresh_token_abcdefghij123456789",
            "access_token": "access_token_abcdefghij123456789"
        }
        self.assertDictEqual(expected_data, login_dict)

    def test_is_expired_return_true(self):
        """Test is_expired should return True when the date is before now"""
        source = {
            "expires_at": 1672560000,
            "expires_in": 1234,
            "refresh_token": "refresh_token_abcdefghij123456789",
            "access_token": "access_token_abcdefghij123456789"
        }
        login_info = LoginDetail.from_db(source=source)
        self.assertTrue(login_info.is_expired())

    def test_is_expired_return_false(self):
        """Test is_expired should return False when the date is after now"""
        source = {
            "expires_at": 1735718400,
            "expires_in": 1234,
            "refresh_token": "refresh_token_abcdefghij123456789",
            "access_token": "access_token_abcdefghij123456789"
        }
        login_info = LoginDetail.from_db(source=source)
        self.assertFalse(login_info.is_expired())


if __name__ == '__main__':
    unittest.main()
