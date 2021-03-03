from django.shortcuts import render

# Create your views here.


def content_list(request):
    return render(request, 'App_Content/content_list.html', context={})
