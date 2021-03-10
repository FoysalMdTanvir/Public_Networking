from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required
def Index(request):
    return HttpResponseRedirect(reverse('App_Content:content_list'))
