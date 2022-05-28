from rest_framework.test import APITestCase


class PostRequestsFieldsTest(APITestCase):

    def test_user_registration_fields(self):
        first_user_data = {
            'email': 'test_user@yandex.ru',
            'username': 'test_user',
            'first_name': 'FN_test_user',
            'last_name': 'LN_test_user',
            'password': 'test_password'
        }
        first_user_expected_response_data = {
            'email': 'test_user@yandex.ru',
            'id': 1,
            'username': 'test_user',
            'first_name': 'FN_test_user',
            'last_name': 'LN_test_user'
        }

        second_user_data = {
            'email': 'test_user@yandex.ru',
            'username': 'test_user',
        }
        second_user_expected_response_data = {
            "email": [
                "This email is already used."
            ],
            "username": [
                "This username is already exist."
            ],
            "password": [
                "This field is required."
            ],
            "first_name": [
                "This field is required."
            ],
            "last_name": [
                "This field is required."
            ]
        }

        response = self.client.post(
            'http://localhost/api/users/', first_user_data)
        self.assertEqual(response.data, first_user_expected_response_data)
        response = self.client.post(
            'http://localhost/api/users/', second_user_data)
        self.assertEqual(response.data, second_user_expected_response_data)
