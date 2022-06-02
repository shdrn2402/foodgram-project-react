from rest_framework.test import APITestCase
from users import models
from users.tests import data_for_tests


class UserAndFollowSerializersTest(APITestCase):

    def create_and_get_user(self, user):
        return self.client.post(
            'http://localhost/api/users/',
            data_for_tests.users_data_types.get(user)
        )

    def create_and_get_token(self):
        self.create_and_get_user('correct')
        data = {
            'password':
            data_for_tests.correct_data_user.get('password'),
            'email':
            data_for_tests.correct_data_user.get('email')
        }

        return self.client.post(
            'http://localhost/api/auth/token/login/',
            data
        )

    def get_user_id(self, type):
        user = data_for_tests.users_data_types.get(type)
        return models.User.objects.get(
            username=user.get('username')).id

    def authorize(self):
        get_token_response = self.create_and_get_token().data.get('auth_token')
        token = f'Token {get_token_response}'
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_custom_user_create_serializer(self):
        response = self.create_and_get_user('correct').json()
        data_for_tests.expected_user_create['id'] = response.get('id')
        self.assertEqual(response,
                         data_for_tests.expected_user_create)
        response = self.create_and_get_user('correct').json()
        self.assertEqual(response,
                         (data_for_tests.
                          expected_validation_error_user_create)
                         )
        response = self.create_and_get_user('insufficient').json()
        self.assertEqual(response,
                         (data_for_tests.
                          expected_insufficient_data_user_create)
                         )

    def test_custom_user_serializer(self):
        self.authorize()
        user_id = self.get_user_id('correct')
        data_for_tests.expected_retrieve_user['id'] = user_id
        self.create_and_get_user('correct').json()
        urls_and_data = {
            'http://localhost/api/users/': (data_for_tests.
                                            expected_retrieve_users_list),
            f'http://localhost/api/users/{user_id}/': (data_for_tests.
                                                       expected_retrieve_user),
            'http://localhost/api/users/me/': (data_for_tests.
                                               expected_retrieve_user),
        }

        self.authorize()
        for url, expected in urls_and_data.items():
            with self.subTest(url=url):
                response = self.client.get(url).json()
                self.assertEqual(response, expected)

    def test_follow_serializer(self):
        ...
