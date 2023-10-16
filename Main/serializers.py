from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']
          
    def create(self,validated_data):
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id','user','name','groups_in','email','expense_map']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name','members','expense_map']

class ExpenseSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Expense
        fields = ['id','paid_by','group','description','amount','split_type','date','split_details']


        