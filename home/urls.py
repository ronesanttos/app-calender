from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.calendario, name='calendario'),
    path('eventos-json/', views.eventos_json,name='eventos_json')

]