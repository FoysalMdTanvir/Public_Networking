from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from App_Login.models import UserProfile
from django.contrib.auth.models import User
# Create your views here.


@login_required
def content_list(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = User.objects.filter(username__icontains=search)
    return render(request, 'App_Content/content_list.html', context={'search': search, 'result': result})
