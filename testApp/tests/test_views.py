from django.test import TestCase
from testApp.models import Message
from django.contrib.auth.models import User

USERNAME = 'testUser'
PASSWORD = '123_makarena_123'


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = User.objects.create_user(username=USERNAME, password=PASSWORD)
        Message.objects.create(author=author)

    def test_view_auth(self):
        resp = self.client.get('/auth')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/auth.html')

    def test_view_null(self):
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.redirect_chain), 0)
        last_chain = resp.redirect_chain[-1]
        self.assertEqual(last_chain[1], 302)
        self.assertEqual(last_chain[0], '/auth?next=/')
        self.assertTemplateUsed(resp, 'registration/auth.html')

    def test_view_authorized_null(self):
        login_status = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertEqual(login_status, True)
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.redirect_chain), 0)
        self.client.logout()
        self.assertTemplateUsed(resp, 'message/send.html')

    def test_view_authorized_auth(self):
        login_status = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertEqual(login_status, True)
        resp = self.client.get('/auth', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.redirect_chain), 0)
        last_chain = resp.redirect_chain[-1]
        self.assertEqual(last_chain[1], 302)
        self.assertEqual(last_chain[0], '/')
        self.assertTemplateUsed(resp, 'message/send.html')


