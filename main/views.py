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
	amount = calc_account_value(user)

	return render(request, 'main/dashboard.html', {"amount": amount})


@login_required(login_url='/login')
def balance(request):
	return render(request, 'main/balance.html')


def calc_account_value(user):
	exchange_rate = PLN_ExchangeRate.objects.all()

	currencies = Currencies.objects.filter(owner=user)
	# TODO implement
	# gold_assets = Gold.objects.filter(owner=user)
	# crypto_assets = Crypto.objects.filter(owner=user)
	# shares_assets = Shares.objects.filter(owner=user)

	account_value = 0
	for currency in currencies:
		if currency.currency != "PLN":
			multiplier = exchange_rate.get(currency_code=currency.currency)
			account_value += currency.ballance * multiplier.exchange_rate
		else:
			account_value += currency.ballance

	return "{:.2f}".format(account_value)

