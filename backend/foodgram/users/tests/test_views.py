# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APITestCase
# from users import models


# class RespondCodesTest(APITestCase):

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.correct_data_user = {
#             'email': 'test_user@yandex.ru',
#             'username': 'test_user',
#             'first_name': 'FN_test_user',
#             'last_name': 'LN_test_user',
#             'password': 'test_password',
#         }

#         cls.correct_data_user_2 = {
#             'email': 'test_user_2@yandex.ru',
#             'username': 'test_user_2',
#             'first_name': 'FN_test_user_2',
#             'last_name': 'LN_test_user_2',
#             'password': 'test_password',
#         }

#         cls.insufficient_data_user = {
#             'email': 'test_user@yandex.ru',
#             'username': 'test_user',
#             'first_name': 'FN_test_user',
#             'last_name': 'LN_test_user',
#         }

#         cls.users_data_types = {
#             'correct': RespondCodesTest.correct_data_user,
#             'correct_2': RespondCodesTest.correct_data_user_2,
#             'insufficient': RespondCodesTest.insufficient_data_user,
#         }

#         cls.status_codes = {
#             'ok': status.HTTP_200_OK,
#             'created': status.HTTP_201_CREATED,
#             'no_content': status.HTTP_204_NO_CONTENT,
#             'validation_error': status.HTTP_400_BAD_REQUEST,
#             'auth_error': status.HTTP_401_UNAUTHORIZED,
#             'not_found_error': status.HTTP_404_NOT_FOUND,
#         }

#     def create_and_get_user(self, type):
#         return self.client.post(
#             'http://localhost/api/users/',
#             RespondCodesTest.users_data_types.get(type)
#         )

#     def create_and_get_token(self):
#         self.create_and_get_user('correct')
#         data = {'password':
#                 RespondCodesTest.correct_data_user.get('password'),
#                 'email':
#                 RespondCodesTest.correct_data_user.get('email')
#                 }

#         return self.client.post(
#             'http://localhost/api/auth/token/login/', data
#         )

#     def get_user_id(self, type):
#         username = RespondCodesTest.users_data_types.get(type)
#         return str(models.User.objects.get(
#             username=username.get('username')).id)

#     def authorize(self):
#         get_token_response = self.create_and_get_token().data.get('auth_token')
#         token = f'Token {get_token_response}'
#         self.client.credentials(HTTP_AUTHORIZATION=token)

#     def request_sub_test(self, data, method):
#         for url, expected in data.items():
#             with self.subTest(url=url):
#                 if method == 'get':
#                     response = self.client.get(url)
#                 if method == 'post':
#                     response = self.client.post(url)
#                 if method == 'delete':
#                     response = self.client.delete(url)
#                 self.assertEqual(response.status_code, expected)

#     def test_get_users_list(self):
#         response = self.client.get('http://localhost/api/users/')
#         self.assertEqual(response.status_code,
#                          RespondCodesTest.status_codes.get('ok'))

#     def test_create_user(self):
#         data_types = {
#             'correct':
#             RespondCodesTest.status_codes.get('created'),
#             'insufficient':
#             RespondCodesTest.status_codes.get('validation_error')
#         }

#         for data_type, expected in data_types.items():
#             with self.subTest(data_type=data_type):
#                 response = self.create_and_get_user(data_type)
#                 self.assertEqual(response.status_code, expected)

#     def test_unauthorized_user_profile(self):
#         urls_and_status_codes = {
#             'http://localhost/api/users/1/':
#             RespondCodesTest.status_codes.get('auth_error'),
#             'http://localhost/api/users/me/':
#             RespondCodesTest.status_codes.get('auth_error'),
#         }

#         self.request_sub_test(urls_and_status_codes, 'get')

#     def test_authorized_user_profile(self):
#         self.authorize()
#         user_id = self.get_user_id('correct')
#         urls_and_status_codes = {
#             'http://localhost/api/users/666/':
#             RespondCodesTest.status_codes.get('not_found_error'),
#             f'http://localhost/api/users/{user_id}/':
#             RespondCodesTest.status_codes.get('ok'),
#             'http://localhost/api/users/me/':
#             RespondCodesTest.status_codes.get('ok'),
#         }
#         self.request_sub_test(urls_and_status_codes, 'get')

#     def test_create_token(self):
#         response = self.create_and_get_token()
#         self.assertEqual(response.status_code,
#                          RespondCodesTest.status_codes.get('created'))

#     def test_destroy_token(self):
#         url = 'http://localhost/api/auth/token/logout/'
#         response = self.client.post(url)
#         self.assertEqual(response.status_code,
#                          RespondCodesTest.status_codes.get('auth_error'))
#         self.authorize()
#         response = self.client.post(url)
#         self.assertEqual(response.status_code,
#                          RespondCodesTest.status_codes.get('no_content'))

#     def test_change_password_url(self):
#         url = 'http://localhost/api/users/set_password/'
#         current_password = RespondCodesTest.correct_data_user.get(
#             'password')
#         new_password = 'new_password'
#         response = self.client.post(url)
#         self.assertEqual(
#             response.status_code,
#             RespondCodesTest.status_codes.get('auth_error')
#         )
#         self.authorize()
#         response = self.client.post(
#             url,
#             {'current_password': current_password})
#         self.assertEqual(
#             response.status_code,
#             RespondCodesTest.status_codes.get('validation_error')
#         )
#         response = self.client.post(
#             url,
#             {'current_password': current_password,
#              'new_password': new_password})
#         self.assertEqual(
#             response.status_code,
#             RespondCodesTest.status_codes.get('no_content')
#         )

#     def test_retrieve_subscribes_list(self):
#         url = 'http://localhost/api/users/subscriptions/'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code,
#                          RespondCodesTest.status_codes.get('auth_error')
#                          )
#         self.authorize()
#         response = self.client.get(url)
#         self.assertEqual(response.status_code,
#                          RespondCodesTest.status_codes.get('ok')
#                          )

#     def test_subscribe(self):
#         user = self.create_and_get_user('correct')
#         author = self.create_and_get_user('correct_2')
#         user_id = user.data.get('id')
#         author_id = author.data.get('id')

#         url = f'http://localhost/api/users/{author_id}/subscribe/'
#         response = self.client.post(url)
#         self.assertEqual(response.status_code,
#                          RespondCodesTest.status_codes.get('auth_error')
#                          )

#         self.authorize()

#         urls_and_status_codes = {
#             f'http://localhost/api/users/{user_id}/subscribe/':
#             RespondCodesTest.status_codes.get('validation_error'),

#             'http://localhost/api/users/666/subscribe/':
#             RespondCodesTest.status_codes.get('not_found_error'),

#             f'http://localhost/api/users/{author_id}/subscribe/':
#             RespondCodesTest.status_codes.get('created'),

#             f'http://localhost/api/users/{author_id}/subscribe/':
#             RespondCodesTest.status_codes.get('validation_error')
#         }

#         self.request_sub_test(urls_and_status_codes, 'post')

#     def test_destroy_subscribtion(self):
#         author = self.create_and_get_user('correct_2')
#         author_id = author.data.get('id')

#         url = f'http://localhost/api/users/{author_id}/subscribe/'
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code,
#                          RespondCodesTest.status_codes.get('auth_error')
#                          )

#         self.authorize()
#         self.client.post(f'http://localhost/api/users/{author_id}/subscribe/')

#         urls_and_status_codes = {
#             'http://localhost/api/users/666/subscribe/':
#             RespondCodesTest.status_codes.get('not_found_error'),

#             f'http://localhost/api/users/{author_id}/subscribe/':
#             RespondCodesTest.status_codes.get('no_content'),

#             f'http://localhost/api/users/{author_id}/subscribe/':
#             RespondCodesTest.status_codes.get('validation_error')
#         }

#         self.request_sub_test(urls_and_status_codes, 'delete')
