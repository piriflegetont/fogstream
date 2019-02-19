from django.test import TestCase
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

USERNAME = 'testUser'
PASSWORD = '123_makarena_123'

USERNAME2 = 'testUser2'
PASSWORD2 = '123_aiaiaiaa_123'


class RegistrationApiTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=USERNAME, password=PASSWORD)

    def test_api_registration_not_ajax(self):
        auth_data = {"login": USERNAME2, "password": PASSWORD2, "repeat_password": PASSWORD2}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Wrong type of request. Use POST ajax request.")

    def test_api_registration_get(self):
        resp = self.client.get('/register')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Wrong type of request. Use POST ajax request.")

    def test_api_registration_existing(self):
        auth_data = {"login": USERNAME, "password": PASSWORD, "repeat_password": PASSWORD}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Такой пользователь уже зарегистрирован")

    def test_api_registration_different_passwords(self):
        auth_data = {"login": USERNAME2, "password": PASSWORD2, "repeat_password": PASSWORD}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Пароль не совпадает с подтверждением")

    def test_api_registration_short_login(self):
        auth_data = {"login": USERNAME[:3], "password": PASSWORD, "repeat_password": PASSWORD}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Логин должен быть длиннее трёх символов.")

    def test_api_registration_long_login(self):
        auth_data = {"login": USERNAME * 20, "password": PASSWORD, "repeat_password": PASSWORD}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Логин должен быть короче двадцати символов.")

    def test_api_registration_bad_mask_login(self):
        auth_data = {"login": 'МойДядя', "password": PASSWORD, "repeat_password": PASSWORD}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Логин должен состоять из английских букв, цифр или знаков подчёркивания")

    def test_api_registration_bad_mask_password(self):
        auth_data = {"login": USERNAME2, "password": 'самыхЧестных', "repeat_password": 'самыхЧестных'}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Пароль должен состоять из английских букв, цифр или знаков подчёркивания")

    def test_api_registration_common_password(self):
        auth_data = {"login": USERNAME2, "password": 'admin', "repeat_password": 'admin'}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Пароль должен состоять из английских букв, цифр или знаков подчёркивания")

    def test_api_registration_short_password(self):
        auth_data = {"login": USERNAME2, "password": PASSWORD2[:2], "repeat_password": PASSWORD2[:2]}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Пароль должен состоять из английских букв, цифр или знаков подчёркивания")

    def test_api_registration_correct(self):
        auth_data = {"login": USERNAME2, "password": PASSWORD2, "repeat_password": PASSWORD2}
        resp = self.client.post('/register', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, False)
        self.assertEqual('url' in body, True)
        self.assertEqual(body['url'], '/auth')
