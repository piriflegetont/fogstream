from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, password_validation
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from smtplib import SMTPException
from .models import Message
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import json
import re


def send_message(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    body = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        try:
            if not len(body['email']) > 0:
                return JsonResponse({"error": "Введите email"})
            if not len(body['email']) >= 200:
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
            return HttpResponse(msg)
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


@login_required(login_url='/auth')
def send_form(request):
    return render(request, 'message/send.html', {})


def e_login(request):
    if request.method == 'POST':
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
    else:
        return JsonResponse({"error": "Wrong type of request. Use POST."})


def e_logout(request):
    logout(request)
    return JsonResponse({"url": '/auth'})


def e_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    body = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        user = User.objects.filter(username=body['login'])
        if user.exists():
            return JsonResponse({"error": "Такой пользователь уже зарегистрирован"})
        try:
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


def auth(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'registration/auth.html', {})
