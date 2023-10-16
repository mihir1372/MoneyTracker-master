from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    groups_in=models.ManyToManyField('Group',related_name='groups_in',default=[])
    expense_map=models.JSONField()
    def __str__(self):
        return self.user.username

class Group(models.Model):
    name = models.CharField(max_length=100, blank=True)
    members=models.ManyToManyField(UserProfile,related_name='members')
    expense_map=models.JSONField()
    def __str__(self):
        return self.name


class Expense(models.Model):
    group=models.CharField(max_length=100, blank=True,default="Self")
    description = models.CharField(max_length=100, blank=True)
    amount = models.FloatField()
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE)    
    split_type = models.CharField(max_length=100)
    date =  models.CharField(max_length=100)
    split_details = models.JSONField()
   
    def __str__(self):
        return self.description




