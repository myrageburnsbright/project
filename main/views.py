from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title': 'Home',
        'content':'Main page - home',
        'list':['first', 'second'],
        'dict': {'first':1, },
        'bool':True
    }
    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse('About page')