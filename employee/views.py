from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Employee, Attendance, Timestamps
from django.contrib.auth import logout
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
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

    if request.method == 'POST':

        dataDate = request.POST.get('date')
        print(dataDate)
    else:
        dataDate = timezone.now().date()
    print(dataDate)
    timestamps = Timestamps.objects.all().filter(
        loginTime__date=dataDate).order_by('modifiedOn')
    
    count = Timestamps.objects.values(
        'emp_id').distinct().count()

    print(count, "------------------")
    print(len(timestamps))
    print(timestamps)
    # Group timestamps by emp_id
    timestamps_by_emp = {}
    for ts in timestamps:
        if ts.emp_id not in timestamps_by_emp:
            timestamps_by_emp[ts.emp_id] = []
        timestamps_by_emp[ts.emp_id].append(ts)

    # Calculate total working hours for each emp_id
    total_working_hours = []
    for emp_id, ts_list in timestamps_by_emp.items():
        latest_ts = ts_list[-1]  # Get the latest entry for emp_id
        login_time = None
        total_work_time = timedelta(hours=0, minutes=0, seconds=0)
        for ts in ts_list:
            if ts.state == 'is_connected':
                login_time = ts.loginTime
            elif ts.state == 'is_disconnected' and login_time is not None:
                logout_time = ts.loginTime
                work_time = logout_time - login_time
                total_work_time += work_time
                login_time = None
        print("=========================", latest_ts.loginTime, logout_time, latest_ts.state,
              total_work_time, latest_ts.emp_id)
        if total_work_time > timedelta(hours=6, minutes=0, seconds=0):
            attendance = "Present"
        else:
            attendance = "Absent"
        if total_work_time:

            total_working_hours.append({'date': dataDate, 'hours': total_work_time,
                                        'firstLogin': latest_ts.loginTime, 'lastLogout': logout_time, 'attendance': attendance, 'emp_id': emp_id})
    print(total_working_hours)
    return render(request, 'home.html', {'data': total_working_hours})


@login_required(login_url='login')
def emp_list(request):
    employee = Employee.objects.all()
    return render(request, 'emp_list.html', {'employee': employee})


@login_required(login_url='login')
def attendance(request):
    id = request.GET.get('id')
    print(id)
    emp = Attendance.objects.all().filter(emp_id=id)
    timestamps = Timestamps.objects.all().filter(emp_id=id).order_by('loginTime')
    print(len(timestamps))
    # print(emp.date)
    # for time in timestamps:
    # Group timestamps by date
    timestamps_by_date = {}
    for ts in timestamps:
        ts_date = ts.loginTime.date()
        if ts_date not in timestamps_by_date:
            timestamps_by_date[ts_date] = []
        timestamps_by_date[ts_date].append(ts)

    # Calculate total working hours for each date
    total_working_hours = []
    total_work_time = timedelta(hours=0, minutes=0, seconds=0)
    for date, ts_list in timestamps_by_date.items():
        login_time = None
        total_work_time = timedelta(hours=0, minutes=0, seconds=0)
        for ts in ts_list:
            if ts.state == 'is_connected':
                login_time = ts.loginTime
            elif ts.state == 'is_disconnected' and login_time is not None:
                logout_time = ts.loginTime
                work_time = logout_time - login_time
                total_work_time += work_time
                login_time = None
            print(ts.loginTime, ts.state, total_work_time)
    if (total_work_time > timedelta(hours=6, minutes=0, seconds=0)):
        attendance = "Present"
    else:
        attendance = "Absent"
    if (total_work_time):
        total_working_hours.append(
            {'date': date, 'hours': total_work_time, 'firstLogin': ts_list[0].loginTime, 'lastLogout': logout_time, 'attendance': attendance})
    print(total_working_hours)
    return render(request, 'emp_attendance.html', {'employee': emp, 'attendance': total_working_hours},)


@login_required(login_url='login')
def addEmployee(request):
    if request.method == "POST":
        name = request.POST.get('name')
        id = request.POST.get('id')
        token = request.POST.get('token')
        Employee.objects.all()
        emp = Employee(emp_id=id, name=name, token=token)
        emp.save()
    return render(request, 'add_emp.html')

@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        emp_id = data.get('emp_id')
        token = data.get('token')
        status = data.get('status')
        
        employee = Employee.objects.filter(emp_id=emp_id, token=token).first()
        if employee:
            if status == 'login':
                Attendance.objects.create(
                    emp_id=emp_id,
                    token=token,
                    loginTime=datetime.now(),
                    status='active'
                )
            elif status == 'logout':
                attendance = Attendance.objects.filter(emp_id=emp_id, token=token, status='active').last()
                if attendance:
                    attendance.logoutTime = datetime.now()
                    attendance.status = 'inactive'
                    attendance.save()
            
            return JsonResponse({"message": "Attendance updated"}, status=200)
        return JsonResponse({"error": "Employee not found"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def logout_view(request):
    logout(request)
    return redirect('login')
