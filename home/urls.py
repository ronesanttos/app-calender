from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.calendario, name='index'),
    path('eventos-json/', views.eventos_json,name='eventos_json'),
    
    path('register/', views.register_api, name='register'),
    path('login/', views.login_api, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update_user/', views.update_user, name='update_user'),
]