from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.conf import settings

# Create your views here.
@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    return render(request, template_name)