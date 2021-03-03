from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, logout

from . import forms

# Create your views here.
class SignUP(CreateView):
    #using default django UserCreateForm
    form_class = forms.UserCreateForm
    #after signup, go to reverse-lazy
    success_url = reverse_lazy('login')

    template_name = 'accounts/signup.html'

##login View and Logout views are already done by authorization from django
