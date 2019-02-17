from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from smtplib import SMTPException
from .models import Message
from django.utils import timezone
from django.core.mail import send_mail
import json
import re


@login_required
def send_message(request):
    body = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        try:
            User.objects.get(email=body['email'])
            subject, from_email, to = re.sub("[\n\r]", '', body['text'][:20]), None, body['email']
            html_content = body['text']
            msg = send_mail(subject, html_content, from_email, [to])
            message = Message(author=request.user)
            message.email = body['email']
            message.text = body['text']
            message.published_date = timezone.now()
            message.status = "Доставлено"
            message.save()
            return HttpResponse(msg)
        except User.DoesNotExist:
            return JsonResponse({"error": "There is no user with such email"})
        except SMTPException:
            message = Message(author=request.user)
            message.email = body['email']
            message.text = body['text']
            message.published_date = timezone.now()
            message.status = "Ошибка при доставке"
            message.save()
            return JsonResponse({"error": "SMTP exception"})
    else:
        return JsonResponse({"error": "Wrong type of request. Use POST."})


def e_handler404(request, *args, **argv):
    response = render(request, '404.html', status=404)
    return response


def e_handler500(request, *args, **argv):
    response = render(request, '500.html', status=500)
    return response


@login_required
def send_form(request):
    return render(request, 'message/send.html', {})


@login_required
def auth(request):
    return render(request, 'registration/auth.html', {})
