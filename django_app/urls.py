from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('mainapp.urls')),
    path('licapi/', include('licapi.urls')),
    path('admin/', admin.site.urls),
]
