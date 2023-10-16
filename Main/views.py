from rest_framework import response,mixins,generics
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .utilities import *

from rest_framework.authtoken.models import Token

# To authenticate the user
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# To Login
from rest_framework.authtoken import views 


# Create your views here.
class RegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return response.Response({'status':403,'errors':serializer.errors,'message':'Oops'})
            
        user = serializer.save()
        
        token,_ = Token.objects.get_or_create(user=user)
          
        return response.Response({'status':200,'user':serializer.data,'token':str(token),'message':'User created successfully'})

'''
class LoginView(APIView):
Done using from rest_framework.authtoken import views
'''

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return response.Response(status=200)

class AuthUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
        token=request.auth
        user = Token.objects.get(key=token).user
        serializer=UserSerializer(user)
        # return response.Response({'user':serializer.data})
        return response.Response({'token':token.key,'user':serializer.data})


class UserProfileApiView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user = Token.objects.get(key=request.auth).user
        data={'user':user.id,'name':request.data['name'],'email':request.data['email'],'expense_map':{"owed":0,"borrowed":0}}
        serializer = UserProfileSerializer(data=data)
        
       
        if UserProfile.objects.filter(user=user).exists():
            return response.Response({'status':403,'message':'User Profile already exists'})
        else:
            if not serializer.is_valid():
                return response.Response({'status':403,'errors':serializer.errors,'message':'Oops'})
            user = serializer.save()
        return response.Response({'status':200,'payload':serializer.data,'message':'User Profile created successfully'})
    
    def get(self,request):
        users=UserProfile.objects.all()
        # groups=Group.objects.all()
        serializer=UserProfileSerializer(users,many=True)
        return response.Response({'status':200,'payload':serializer.data,'message':'Groups fetched successfully'})

    
class UserProfileDetailApiView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = UserProfileSerializer
    lookup_field=('user')
    
    def get_queryset(self):
        id=self.kwargs.get(self.lookup_field)
        return UserProfile.objects.filter(user=id)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GroupApiView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        try:
            members=list(map(int,str(dict(request.data)['members']).split(',')))
        except:
            members=list(map(int,str(dict(request.data)['members'][0]).split(',')))
        print(members)
        data={'name':request.data['name'],'members':members,'expense_map':{'expenses':[]}}
        serializer = GroupSerializer(data=data)
        
       
        if not serializer.is_valid():
            return response.Response({'status':403,'errors':serializer.errors,'message':'Oops'})
        group = serializer.save()

        for i in data['members']:
            user_profile=UserProfile.objects.get(id=int(i))
            user_profile.groups_in.add(group.id)
       
        groups=user_profile.groups_in.all()
        groupSerializer=GroupSerializer(groups,many=True)

        return response.Response({'status':200,'payload':groupSerializer.data,'message':'Group created successfully'})
        # return response.Response({'status':200})
        
    def get(self,request):
        user = Token.objects.get(key=request.auth).user
        user_profile=UserProfile.objects.get(user=user)
        groups=user_profile.groups_in.all()
        # groups=Group.objects.all()
        serializer=GroupSerializer(groups,many=True)
        return response.Response({'status':200,'payload':serializer.data,'message':'Groups fetched successfully'})
    

class GroupDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    
        authentication_classes = [TokenAuthentication]
        permission_classes=[IsAuthenticated]
        serializer_class = GroupSerializer
        lookup_field=('id')
        
        def get_queryset(self):
            id= self.kwargs.get(self.lookup_field)
            return Group.objects.filter(id=id)
        
        def put(self, request, *args, **kwargs):
            return self.partial_update(request, *args, **kwargs)
        

class ExpenseApiView(APIView):
   
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        split_type=request.data['split_type']
        split_details=request.data['split_details']
        amount=request.data['amount']
        paid_by=request.data['paid_by']
        

        new_split_details=expense_split_check(paid_by,split_type,split_details,amount)
        if new_split_details==False:
            return response.Response({'status':403,'message':'Oops'})
        
        data={
            'paid_by':User.objects.get(id=int(paid_by)).id,
            'group':Group.objects.get(id=(request.data['group'])).id,
            'description':request.data['description'],
            'amount':amount,
            'split_type':split_type,
            'date':request.data['date'],
            'split_details':new_split_details
        }

        serializer = ExpenseSerializer(data=data)
        if not serializer.is_valid():
            return response.Response({'status':403,'errors':serializer.errors,'message':'Oops'})
        expense = serializer.save()
        
        group_balance_sheet.delay(serializer.data['group'])
       
        return response.Response({'status':200,'payload':serializer.data,'message':'Expense Added successfully'})


class GroupExpenseApiView(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = ExpenseSerializer
    lookup_field=('id')
    
    def get_queryset(self):
        id = self.kwargs.get(self.lookup_field)
        expenses=Expense.objects.filter(group=id)

        return expenses
        


class GroupBalanceSheetApiView(APIView):
    def post(self,request):
        group_id=request.data['group_id']
        group=Group.objects.get(id=group_id)
        members=group.members.all()
        balance_sheet={}
        for i in members:
            balance_sheet[i.username]=0
        expenses=Expense.objects.filter(group=group)
        for i in expenses:
            for j in i.split_details:
                if j['user']==i.paid_by.username:
                    balance_sheet[j['user']]-=j['amount']
                else:
                    balance_sheet[j['user']]+=j['amount']
        return response.Response({'status':200,'payload':balance_sheet,'message':'Balance Sheet fetched successfully'})
 

class ExpenseDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    
        authentication_classes = [TokenAuthentication]
        permission_classes=[IsAuthenticated]
        serializer_class = ExpenseSerializer
        lookup_field=('id')
        
        def get_queryset(self):
            id= self.kwargs.get(self.lookup_field)
            expense=Expense.objects.filter(id=id)
            group_balance_sheet.delay(expense[0].group)
            return expense
        
        def put(self, request, *args, **kwargs):
            id= self.kwargs.get(self.lookup_field)
            expense=Expense.objects.filter(id=id)
            group_balance_sheet.delay(expense[0].group)
            return self.partial_update(request, *args, **kwargs)


    