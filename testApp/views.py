from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def e_handler404(request, *args, **argv):
    response = render(request, '404.html', status=404)
    return response


def e_handler500(request, *args, **argv):
    response = render(request, '500.html', status=500)
    return response


@login_required(login_url='/auth')
def send_form(request):
    return render(request, 'message/send.html', {})


def auth(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'registration/auth.html', {})
