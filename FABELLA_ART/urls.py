from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', include('app1.urls')),  
    path('admin_login/', admin.site.urls),
    path('admin/', admin.site.urls),
    
    
]