from django.urls import path

from account.api.views import *

app_name = 'account'

urlpatterns = [
    path('signup', registration_view, name='register'),
    path('login', TokenObtainView.as_view(), name='login'),
]