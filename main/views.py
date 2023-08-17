from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . models import Currencies


def start_page(request):
	return redirect('/login')


def logout_user(request):
	logout(request)


@login_required(login_url='/login')
def dashboard(request):
	user = request.user
	balance = Currencies.objects.get(id=user.id)
	amount = balance.ballance
	return render(request, 'main/dashboard.html', {"amount": amount})

@login_required(login_url='/login')
def balance(request):
	return render(request, 'main/balance.html')

