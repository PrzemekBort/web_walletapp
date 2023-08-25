from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

import datetime
import requests


# Create your models here.

class Currencies(models.Model):

    CURRENCIES = [
        ("PLN", "Polish Zloty"),
        ("USD", "United States Dolar"),
        ("EUR", "Euro"),
        ("GBP", "Great British Pound"),
        ("CHF", "Swiss Franc"),
        ("CNY", "Chinese Yuan Renminbi"),
        ("JPY", "Japanese Yen")
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    ballance = models.FloatField(default=0)
    main_currency = models.BooleanField(default=False)

    def get_exchange_rate(self):
        if self.currency != "PLN":
            currency = PLN_ExchangeRate.objects.get(currency_code=self.currency)
            return currency.exchange_rate
        else:
            return 1.0

    def get_value_in_PLN(self):
        if self.currency != "PLN":
            multiplier = float(self.get_exchange_rate())
            ballance = getattr(self, "ballance")
            return "{:.2f}".format(ballance * multiplier)
        else:
            return "{:.2f}".format(self.ballance)


class BaseAsset(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    _quantity = models.FloatField(default=0)
    _buy_price = models.FloatField()
    buy_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Gold(BaseAsset):

    GOLD_TYPE = [
        ("BC", "Bullion Coin"),
        ("GB", "Gold Bar"),
        ("CT", "Contract")
    ]

    gold_type = models.CharField(max_length=2, choices=GOLD_TYPE)
    origin = models.CharField(max_length=30)
    fineness = models.PositiveIntegerField(
        default=999,
        validators=[
            MaxValueValidator(999)
        ]
    )


class Crypto(BaseAsset):

    storage_place = models.CharField(max_length=30)


class Shares(BaseAsset):

    SHARES_TYPE = [
        ("SHR", "Share"),
        ("ETF", "ETF")
    ]

    shares_type = models.CharField(
        max_length=5,
        choices=SHARES_TYPE)
    market = models.CharField(max_length=30)
    ticker = models.CharField(max_length=30)
    industry = models.CharField(max_length=100)
    dividend_yield = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ]
    )


class PLN_ExchangeRate(models.Model):

    CURRENCIES = [
        ("USD", "United States Dolar"),
        ("EUR", "Euro"),
        ("GBP", "Great British Pound"),
        ("CHF", "Swiss Franc"),
        ("CNY", "Chinese Yuan Renminbi"),
        ("JPY", "Japanese Yen")
    ]

    currency_code = models.CharField(max_length=3, choices=CURRENCIES)  # TODO implement unique
    exchange_rate = models.FloatField()
    last_updated = models.DateTimeField()

    def update(self):
        body = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/a/'
                            f'{self.currency_code}/')  # lowercased currency code USD -> usd
        response = body.json()

        self.exchange_rate = float(response['rates'][0]['mid'])
        self.last_updated = datetime.datetime.now()
        self.save()

    def __str__(self):
        return self.currency_code
