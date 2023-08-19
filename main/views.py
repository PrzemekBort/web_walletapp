from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *


def start_page(request):
    return redirect('/login')


def logout_user(request):
    logout(request)


@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    amount = account_value(user)
    count = assets_count(user)

    return render(request, 'main/dashboard.html',
                  context={
                      "amount": amount,
                      "assets_count": count}
                  )


@login_required(login_url='/login')
def balance(request):
    return render(request, 'main/balance.html')


# ----- CUSTOM FUNCTIONS ----- #
def account_value(user):
    exchange_rate = PLN_ExchangeRate.objects.all()

    currencies = Currencies.objects.filter(owner=user)
    # TODO implement
    # gold_assets = Gold.objects.filter(owner=user)
    # crypto_assets = Crypto.objects.filter(owner=user)
    # shares_assets = Shares.objects.filter(owner=user)

    value = 0  # sumarize account value
    for currency in currencies:
        if currency.currency != "PLN":
            multiplier = exchange_rate.get(currency_code=currency.currency)
            value += currency.ballance * multiplier.exchange_rate
        else:
            value += currency.ballance

    return "{:.2f}".format(value)


def assets_count(user):
    currencies = Currencies.objects.filter(owner=user).count()
    gold_assets = Gold.objects.filter(owner=user).count()
    crypto_assets = Crypto.objects.filter(owner=user).count()
    shares_assets = Shares.objects.filter(owner=user).count()

    return currencies + gold_assets + crypto_assets + shares_assets
