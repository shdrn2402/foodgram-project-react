from rest_framework import status
from rest_framework.test import APITestCase
from users import models
from users.tests import data_for_tests


class RespondCodesTest(APITestCase):

    def create_and_get_user(self, type):
        return self.client.post(
            'http://localhost/api/users/',
            data_for_tests.users_data_types.get(type)
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
        return str(models.User.objects.get(
            username=user.get('username')).id)

    def authorize(self):
        get_token_response = self.create_and_get_token().data.get('auth_token')
        token = f'Token {get_token_response}'
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def request_sub_test(self, data, method):
        for url, expected in data.items():
            with self.subTest(url=url):
                if method == 'get':
                    response = self.client.get(url)
                if method == 'post':
                    response = self.client.post(url)
                if method == 'delete':
                    response = self.client.delete(url)
                self.assertEqual(response.status_code, expected)

    def test_get_users_list(self):
        response = self.client.get('http://localhost/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data_types = {
            'correct': status.HTTP_201_CREATED,
            'insufficient': status.HTTP_400_BAD_REQUEST
        }

        for data_type, expected in data_types.items():
            with self.subTest(data_type=data_type):
                response = self.create_and_get_user(data_type)
                self.assertEqual(response.status_code, expected)

    def test_unauthorized_user_profile(self):
        urls_and_status_codes = {
            'http://localhost/api/users/1/': status.HTTP_401_UNAUTHORIZED,
            'http://localhost/api/users/me/': status.HTTP_401_UNAUTHORIZED,
        }

        self.request_sub_test(urls_and_status_codes, 'get')

    def test_authorized_user_profile(self):
        self.authorize()
        user_id = self.get_user_id('correct')
        urls_and_status_codes = {
            'http://localhost/api/users/666/': status.HTTP_404_NOT_FOUND,
            f'http://localhost/api/users/{user_id}/': status.HTTP_200_OK,
            'http://localhost/api/users/me/': status.HTTP_200_OK,
        }
        self.request_sub_test(urls_and_status_codes, 'get')

    def test_create_token(self):
        response = self.create_and_get_token()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_token(self):
        url = 'http://localhost/api/auth/token/logout/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.authorize()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_change_password_url(self):
        url = 'http://localhost/api/users/set_password/'
        current_password = data_for_tests.correct_data_user.get(
            'password')
        new_password = 'new_password'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.authorize()
        response = self.client.post(
            url,
            {'current_password': current_password}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            url,
            {'current_password': current_password,
             'new_password': new_password}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_subscribes_list(self):
        url = 'http://localhost/api/users/subscriptions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.authorize()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscribe(self):
        user = self.create_and_get_user('correct')
        author = self.create_and_get_user('correct_2')
        user_id = user.data.get('id')
        author_id = author.data.get('id')

        url = f'http://localhost/api/users/{author_id}/subscribe/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.authorize()
        urls_and_status_codes = {
            f'http://localhost/api/users/{user_id}/subscribe/':
            status.HTTP_400_BAD_REQUEST,

            'http://localhost/api/users/666/subscribe/':
            status.HTTP_404_NOT_FOUND,

            f'http://localhost/api/users/{author_id}/subscribe/':
            status.HTTP_201_CREATED,

            f'http://localhost/api/users/{author_id}/subscribe/':
            status.HTTP_400_BAD_REQUEST
        }

        self.request_sub_test(urls_and_status_codes, 'post')

    def test_destroy_subscribtion(self):
        author = self.create_and_get_user('correct_2')
        author_id = author.data.get('id')

        url = f'http://localhost/api/users/{author_id}/subscribe/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.authorize()
        self.client.post(f'http://localhost/api/users/{author_id}/subscribe/')

        urls_and_status_codes = {
            'http://localhost/api/users/666/subscribe/':
            status.HTTP_404_NOT_FOUND,

            f'http://localhost/api/users/{author_id}/subscribe/':
            status.HTTP_204_NO_CONTENT,

            f'http://localhost/api/users/{author_id}/subscribe/':
            status.HTTP_400_BAD_REQUEST
        }

        self.request_sub_test(urls_and_status_codes, 'delete')
