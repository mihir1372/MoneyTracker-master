from django.urls import path,include
from . import views
from .login import *




urlpatterns = [
    # path('', views.home),

    path("register/",views.RegisterView.as_view()),
    path("login/",ObtainAuthToken.as_view()),
    path("logout/",views.Logout.as_view()),
    path('user/', views.AuthUserAPIView.as_view(),name="User"), # Returns token

    path('userprofile/', views.UserProfileApiView.as_view(),name="UserProfile"),
    path('userprofile/<slug:user>/', views.UserProfileDetailApiView.as_view(),name="UserProfile"),

    path('groups/', views.GroupApiView.as_view()),
    path('groups/<int:id>/', views.GroupDetailApiView.as_view()),
    
    path('expense/', views.ExpenseApiView.as_view()),
    path('expense/<int:id>/', views.ExpenseDetailApiView.as_view()),

    path('groupexpense/<int:id>/', views.GroupExpenseApiView.as_view()),

    path('groupbalancesheet/', views.GroupBalanceSheetApiView.as_view()),
    
    
]