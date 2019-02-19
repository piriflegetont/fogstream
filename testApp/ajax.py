from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from smtplib import SMTPException
from .models import Message
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import json
import re


def send_message(request):
    if request.method != 'POST' or not request.is_ajax():
        return JsonResponse({"error": "Wrong type of request. Use POST ajax request."})
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    try:
        body = json.loads(request.body.decode("utf-8"))
        if not len(body['email']) > 0:
            return JsonResponse({"error": "Введите email"})
        if len(body['email']) >= 200:
            return JsonResponse({"error": "Слшиком длинный email. Максимум 200 символов"})
        user = User.objects.filter(email=body['email'])
        user = user.filter(is_superuser=True)
        if not user.exists():
            return JsonResponse({"error": "Администратора с такой электронной почтой не существует"})
        subject, from_email, to = re.sub("[\n\r]", '', body['text'][:20]), None, body['email']
        html_content = body['text']
        msg = send_mail(subject, html_content, from_email, [to])
        message = Message(author=request.user)
        message.email = body['email']
        message.text = body['text']
        message.published_date = timezone.now()
        message.status = "Доставлено"
        message.save()
        return JsonResponse({"url": "/", "msg": msg})
    except SMTPException as e:
        message = Message(author=request.user)
        message.email = body['email']
        message.text = body['text']
        message.published_date = timezone.now()
        message.status = "Ошибка при доставке"
        message.save()
        return JsonResponse({"error": "SMTP exception", "msg": str(e)})


def e_login(request):
    if request.method != 'POST' or not request.is_ajax():
        return JsonResponse({"error": "Wrong type of request. Use POST ajax request."})
    try:
        body = json.loads(request.body.decode("utf-8"))
        username = body['login']
        password = body['password']
        if not len(username) > 0:
            return JsonResponse({"error": "Введите логин"})
        if not len(password) > 0:
            return JsonResponse({"error": "Введите пароль"})
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({"error": "Такого пользователя нет!"})
        if user.is_active:
            login(request, user)
            return JsonResponse({"url": '/'})
        else:
            return JsonResponse({"error": "Пользователь не доступен"})
    except:
        return JsonResponse({"error": "Unknown error in login"})


def e_logout(request):
    if request.method != 'POST' or not request.is_ajax():
        return JsonResponse({"error": "Wrong type of request. Use POST ajax request."})
    try:
        logout(request)
        return JsonResponse({"url": '/auth'})
    except:
        return JsonResponse({"error": "Unknown error in logout"})


def e_register(request):
    if request.method != 'POST' or not request.is_ajax():
        return JsonResponse({"error": "Wrong type of request. Use POST ajax request."})
    try:
        body = json.loads(request.body.decode("utf-8"))
        user = User.objects.filter(username=body['login'])
        if user.exists():
            return JsonResponse({"error": "Такой пользователь уже зарегистрирован"})
        if body['password'] != body['repeat_password']:
            raise ValidationError("Пароль не совпадает с подтверждением")
        if not len(body['login']) > 3:
            raise ValidationError("Логин должен быть длиннее трёх символов.")
        if not len(body['login']) < 20:
            raise ValidationError("Логин должен быть короче двадцати символов.")
        if not re.match(r'[A-Za-z0-9_]{3,20}', body['login']):
            raise ValidationError("Логин должен состоять из английских букв, цифр или знаков подчёркивания")
        if not re.match(r'[A-Za-z0-9_]{8,}', body['password']):
            raise ValidationError("Пароль должен состоять из английских букв, цифр или знаков подчёркивания")
        password_validation.CommonPasswordValidator().validate(password=body['password'])
        password_validation.MinimumLengthValidator().validate(password=body['password'])
        User.objects.create_user(username=body['login'],  password=body['password'])
        return JsonResponse({"url": "/auth"})
    except ValidationError as e:
        return JsonResponse({"error": '; '.join(e.messages)})
    except:
        return JsonResponse({"error": "Unknown error creating user"})
