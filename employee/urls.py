from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('home', views.home, name='home'),
    path('employeeList', views.emp_list, name='employeeList'),
    path('attendance', views.attendance, name='attendance'),
    path('mark-attendance', views.mark_attendance, name='mark-attendance'),
    path('addEmployee', views.addEmployee, name="addEmployee"),
    path('logout/', views.logout_view, name='logout'),
]
