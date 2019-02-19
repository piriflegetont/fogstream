from django.test import TestCase
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

USERNAME = 'testUser'
PASSWORD = '123_makarena_123'


class LogoutApiTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=USERNAME, password=PASSWORD)

    def test_api_logout_get(self):
        resp = self.client.get('/logout')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Wrong type of request. Use POST ajax request.")

    def test_api_logout_not_ajax(self):
        resp = self.client.post('/logout')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Wrong type of request. Use POST ajax request.")

    def test_api_logout(self):
        login_status = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertEqual(login_status, True)
        resp = self.client.post('/logout', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, False)
        self.assertEqual('url' in body, True)
        self.assertEqual(body['url'], '/auth')
