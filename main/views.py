from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . models import *


def start_page(request):
	return redirect('/login')


def logout_user(request):
	logout(request)


@login_required(login_url='/login')
def dashboard(request):
	user = request.user
	ballance = Currencies.objects.get(id=user.id)
	amount = ballance.ballance
	return render(request, 'main/dashboard.html', {"amount": amount})


@login_required(login_url='/login')
def balance(request):
	return render(request, 'main/balance.html')


def calc_account_value(user):
	currencies = Currencies.objects.filter(id=user.id)
	gold = Gold.objects.filter(id=user.id)
	crypto = Crypto.objects.filter(id=user.id)
	shares = Shares.objects.filter(id=user.id)

