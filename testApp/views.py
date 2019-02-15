from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def post_list(request):
    return render(request, 'message/post_list.html', {})

@login_required
def post_publish(request, pk):
    return redirect('post_list', pk=pk)