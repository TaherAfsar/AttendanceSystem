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
    minsActive = models.IntegerField()
    minsInactive = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

