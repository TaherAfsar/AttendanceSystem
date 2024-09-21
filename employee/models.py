from django.db import models

# Create your models here.


class Employee(models.Model):
    emp_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class Attendance(models.Model):
    emp_id = models.CharField(max_length=100)
    date = models.DateField()
    token = models.CharField(max_length=100)
    loginTime = models.DateTimeField()
    logoutTime = models.DateTimeField()
    # minsActive = models.IntegerField()
    # minsInactive = models.IntegerField()
    # totalHours = models.DateTimeField(default="2023-04-01 12:30:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # is_present = models.BooleanField(default=False)
    status = models.CharField(max_length=7)
    is_deleted = models.BooleanField(default=False)


class Timestamps(models.Model):
    emp_id = models.CharField(max_length=100)
    loginTime = models.DateTimeField()
    modifiedOn = models.DateTimeField()
    state = models.CharField(max_length=100)  # is connected or disconnected
    temp = models.BooleanField(default=False)
