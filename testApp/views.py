from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.http import JsonResponse
from django.utils import timezone


@login_required
def send_message(request):
    if request.method == 'POST':
        response_data = {}
        form = PostForm()
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            response_data = post
        return JsonResponse(response_data)
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


@login_required
def send_form(request):
    return render(request, 'message/send.html', {})
