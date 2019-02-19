from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

USERNAME = 'testUser'
PASSWORD = '123_makarena_123'
ADMINEMAIL = settings.ADMINS[0][1] or 'test.user.django@yandex.ru'
ADMINPASS = 'MeidY0QnhIwn'
MSG = 'Мой дядя самых честных правил когда не в шутку занемог...'


class SendApiTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        User.objects.create_superuser('admin', ADMINEMAIL, password=ADMINPASS)

    def test_api_send_not_ajax(self):
        auth_data = {"login": USERNAME, "password": PASSWORD, "repeat_password": PASSWORD}
        resp = self.client.post('/send', json.dumps(auth_data), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Wrong type of request. Use POST ajax request.")

    def test_api_send_get(self):
        resp = self.client.get('/send')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Wrong type of request. Use POST ajax request.")

    def test_api_send_without_auth(self):
        msg_data = {"email": '', 'text': MSG}
        resp = self.client.post('/send', json.dumps(msg_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 403)

    def test_api_send_email_len_zero(self):
        msg_data = {"email": '', 'text': MSG}
        login_status = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertEqual(login_status, True)
        resp = self.client.post('/send', json.dumps(msg_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Введите email")

    def test_api_send_email_len_200(self):
        msg_data = {"email": ADMINEMAIL * 200, 'text': MSG}
        login_status = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertEqual(login_status, True)
        resp = self.client.post('/send', json.dumps(msg_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Слшиком длинный email. Максимум 200 символов")

    def test_api_send_not_admin(self):
        msg_data = {"email": 'randomdude', 'text': MSG}
        login_status = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertEqual(login_status, True)
        resp = self.client.post('/send', json.dumps(msg_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('error' in body, True)
        self.assertEqual(body['error'], "Администратора с такой электронной почтой не существует")

    def test_api_send_correct(self):
        print()
        msg_data = {"email": ADMINEMAIL, 'text': MSG}
        login_status = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertEqual(login_status, True)
        resp = self.client.post('/send', json.dumps(msg_data), content_type="application/json",
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(isinstance(resp, JsonResponse), True)
        body = json.loads(resp.content.decode("utf-8"))
        self.assertEqual('msg' in body, True)

