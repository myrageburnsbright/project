from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title': 'Home - Главная',
        'content':'Магазин мебели HOME',
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
    'title': 'Home - About us ',
    'content':'About us',
    'text_on_page': "Text about our beatiful page about page"}
        
    return render(request, 'main/about.html', context)