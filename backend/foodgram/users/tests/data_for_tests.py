correct_data_user = {
    'email': 'test_user@yandex.ru',
    'username': 'test_user',
    'first_name': 'FN_test_user',
    'last_name': 'LN_test_user',
    'password': 'test_password',
}
correct_data_user_2 = {
    'email': 'test_user_2@yandex.ru',
    'username': 'test_user_2',
    'first_name': 'FN_test_user_2',
    'last_name': 'LN_test_user_2',
    'password': 'test_password',
}
users_data_types = {
    'correct': correct_data_user,
    'correct_2': correct_data_user_2,
    'insufficient': {}
}
expected_user_create = {
    'email': 'test_user@yandex.ru',
    'username': 'test_user',
    'first_name': 'FN_test_user',
    'last_name': 'LN_test_user'
}
expected_validation_error_user_create = {
    'email': ['This email is already used.'],
    'username': ['This username is already exist.'],
}
expected_insufficient_data_user_create = {
    'email': ['This field is required.'],
    'username': ['This field is required.'],
    'password': ['This field is required.'],
    'first_name': ['This field is required.'],
    'last_name': ['This field is required.']
}

expected_retrieve_user = {
    'email': correct_data_user['email'],
    'username': correct_data_user['username'],
    'first_name': correct_data_user['first_name'],
    'last_name': correct_data_user['last_name'],
    'is_subscribed': False
}

expected_retrieve_users_list = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [expected_retrieve_user]
}
