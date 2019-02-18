from django.test import TestCase
from testApp.models import Message
from django.contrib.auth.models import User


class MessageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = User.objects.create(username='testUser',  password='123_makarena_123')
        Message.objects.create(author=author)

    def test_author_label(self):
        message = Message.objects.get(id=1)
        field_author = message._meta.get_field('author').verbose_name
        print(message)
        self.assertEquals(field_author, 'author')

    def test_email_max_length(self):
        author = Message.objects.get(id=1)
        max_length = author._meta.get_field('email').max_length
        self.assertEquals(max_length, 200)

    def test_status_max_length(self):
        author = Message.objects.get(id=1)
        max_length = author._meta.get_field('status').max_length
        self.assertEquals(max_length, 200)


