from django.db import models
from django.utils import timezone
from django.conf import settings


class Message(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        print(settings.ADMINS)
        self.published_date = timezone.now()
        return {'ADMINS': settings.ADMINS}

    def __str__(self):
        return self.email
