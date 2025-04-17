from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        categories = Categories.objects.all()

        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = 'Магазин мебели HOME'
        context['categories'] = categories

        return context
    
class AboutView(TemplateView):
    template_name = 'main/about.html'
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home - About us'
        context["content"] = 'About us',
        context["text_on_page"] = "Text about our beatiful page about page" 
        return context
    

# def index(request):
#     categories = Categories.objects.all()
#     context = {
#         'title': 'Home - Главная',
#         'content':'Магазин мебели HOME',
#         'categories':categories
#     }
#     return render(request, 'main/index.html', context)

# def about(request):
#     context = {
#     'title': 'Home - About us ',
#     'content':'About us',
#     'text_on_page': "Text about our beatiful page about page"}
        
#     return render(request, 'main/about.html', context)