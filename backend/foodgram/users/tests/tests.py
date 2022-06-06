from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users import models
from users.tests import data_for_tests

'''Прошу совета, что почитать или посмотреть на тему тестирования именно api,
поскольку есть подозрение, что все реализовал не правильно.
Например, как использовать setUp класс, если его вообще надо
использовать (сомнения) при тестировании api.'''


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
        return models.User.objects.get(
            username=user.get('username')).id

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
        user_id = str(self.get_user_id('correct'))
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
        }
        self.request_sub_test(urls_and_status_codes, 'post')

        url = f'http://localhost/api/users/{author_id}/subscribe/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            status.HTTP_204_NO_CONTENT
        }
        self.request_sub_test(urls_and_status_codes, 'delete')


class UsersViewsTest(APITestCase):

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
        return models.User.objects.get(
            username=user.get('username')).id

    def authorize(self):
        get_token_response = self.create_and_get_token().data.get('auth_token')
        token = f'Token {get_token_response}'
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_user_create(self):
        before_create = models.User.objects.all().count()
        self.assertEqual(before_create, 0, 'DB already contains users!')
        self.create_and_get_user('correct')
        after_create = models.User.objects.all().count()
        self.assertEqual(after_create, 1, 'Object did not created!')

    def test_token_create(self):
        before_create = Token.objects.all().count()
        self.assertEqual(before_create, 0, 'DB already contains tokens!')
        self.create_and_get_token()
        after_create = Token.objects.all().count()
        self.assertEqual(after_create, 1, 'Token did not created!')

    def test_follow_create(self):
        before_create = models.Follow.objects.all().count()
        author = self.create_and_get_user('correct_2')
        author_id = author.data.get('id')

        self.assertEqual(before_create, 0, 'DB already contains follows!')
        self.authorize()

        url = f'http://localhost/api/users/{author_id}/subscribe/'
        self.client.post(url)
        after_create = models.Follow.objects.all().count()
        self.assertEqual(after_create, 1, 'Object did not created!')

        self.client.delete(url)
        after_delete = models.Follow.objects.all().count()
        self.assertEqual(after_delete, 0, 'Object did not deleted!')


class UserAndFollowSerializersTest(APITestCase):

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
