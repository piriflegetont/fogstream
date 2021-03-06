from django.test import TestCase
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

USERNAME = 'testUser'
PASSWORD = '123_makarena_123'


class LoginApiTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=USERNAME, password=PASSWORD)

    def test_api_login_not_ajax(self):
        auth_data = {"login": USERNAME, "password": PASSWORD}
        resp = self.client.post('/login', json.dumps(auth_data), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Wrong type of request. Use POST ajax request.")

    def test_api_login_get(self):
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Wrong type of request. Use POST ajax request.")

    def test_api_login_without_username(self):
        auth_data = {"login": "", "password": PASSWORD}
        resp = self.client.post('/login', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Введите логин")

    def test_api_login_without_password(self):
        auth_data = {"login": USERNAME, "password": ''}
        resp = self.client.post('/login', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Введите пароль")

    def test_api_login_stranger(self):
        auth_data = {"login": 'englishmen', "password": 'innewyork'}
        resp = self.client.post('/login', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Такого пользователя нет!")

    def test_api_login_correct(self):
        auth_data = {"login": USERNAME, "password": PASSWORD}
        resp = self.client.post('/login', json.dumps(auth_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, False)
        self.assertEqual('url' in body, True)
        self.assertEqual(body['url'], '/')

