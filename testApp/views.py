from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Message
from django.utils import timezone
from django.core.mail import send_mail
import json


@login_required
def send_message(request):
    body = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        try:
            User.objects.get(email=body['email'])
            print('start')
            subject, from_email, to = 'hello', 'test.testowich.testov@yandex.ru', 'piriflegetont@gmail.com'
            html_content = '<p>This is an <strong>important</strong> message.</p>'
            msg = send_mail(subject, html_content, from_email, [to])
            print('end')
            print(msg)
            #message = Message(author=request.user)
            #message.email = body['email']
            #message.text = body['text']
            #message.published_date = timezone.now()
            #message.save()
            return HttpResponse(answer)
        except User.DoesNotExist:
            print("NONE")
            return JsonResponse({"error": "There is no user with such email"})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


@login_required
def send_form(request):
    return render(request, 'message/send.html', {})
