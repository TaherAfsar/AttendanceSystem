from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee ,Attendance

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            return redirect('home')
        else:
            
            pass
    return render(request, 'registration/login.html')


@login_required(login_url='login')
def home(request):
    employee = Employee.objects.all()
    return render(request, 'home.html',{'employee':employee})

@login_required(login_url='login')
def attendance(request):
    id=request.GET.get('id')
    print(id)
    emp = Attendance.objects.all().filter(emp_id=id)
    print(emp)
    return render(request,'emp_attendance.html',{'emp' : emp})