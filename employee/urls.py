from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('home', views.home, name='home'),
    path('attendance', views.attendance, name='attendance'),
]
