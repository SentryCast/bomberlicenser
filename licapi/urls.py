from django.urls import path
from . import views 

app_name="licapi"
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('reg', views.RegView, name='reg'),
    path('secret_path-connecnted-with-token',
         views.TgBotView, name='tgbot')
]
