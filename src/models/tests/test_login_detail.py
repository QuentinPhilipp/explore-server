import unittest

from models.LoginDetail import LoginDetail


class TestLoginDetail(unittest.TestCase):
    _login_details = LoginDetail(
        1672560000,
        1234,
        "refresh_token_abcdefghij123456789",
        "access_token_abcdefghij123456789"
    )

    def test_from_dict(self):
        source = {
            "expires_at": 1672560000,
            "expires_in": 1234,
            "refresh_token": "refresh_token_abcdefghij123456789",
            "access_token": "access_token_abcdefghij123456789"
        }
        login_info = LoginDetail.from_dict(source=source)
        # Check that LoginDetails constructor works
        self.assertEqual(login_info._refresh_token, "refresh_token_abcdefghij123456789")

    def test_to_dict(self):
        login_dict = self._login_details.to_dict()
        expected_data = {
            "expires_at": 1672560000,
            "expires_in": 1234,
            "refresh_token": "refresh_token_abcdefghij123456789",
            "access_token": "access_token_abcdefghij123456789"
        }
        self.assertDictEqual(expected_data, login_dict)

    def test_is_expired_return_true(self):
        # Date 2023-01-01T08:00:00
        source = {
            "expires_at": 1672560000,
            "expires_in": 1234,
            "refresh_token": "refresh_token_abcdefghij123456789",
            "access_token": "access_token_abcdefghij123456789"
        }
        login_info = LoginDetail.from_dict(source=source)
        self.assertTrue(login_info.is_expired())

    def test_is_expired_return_false(self):
        # Date 2025-01-01T08:00:00
        source = {
            "expires_at": 1735718400,
            "expires_in": 1234,
            "refresh_token": "refresh_token_abcdefghij123456789",
            "access_token": "access_token_abcdefghij123456789"
        }
        login_info = LoginDetail.from_dict(source=source)
        self.assertFalse(login_info.is_expired())


if __name__ == '__main__':
    unittest.main()
