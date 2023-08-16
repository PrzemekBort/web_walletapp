from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def start_page(request):
	return redirect('/login')


def logout_user(request):
	logout(request)


@login_required(login_url='/login')
def dashboard(request):
	return render(request, 'main/dashboard.html')

