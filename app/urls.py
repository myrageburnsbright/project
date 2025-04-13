from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from app import settings
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),  
    path('catalog/', include('goods.urls', namespace='catalog')),    
    path('user/', include('users.urls', namespace='user')),
    path('cart/', include('carts.urls', namespace='cart'))    
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls() 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)