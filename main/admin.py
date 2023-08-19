from django.contrib import admin
from .models import Currencies, PLN_ExchangeRate

# Register your models here.
admin.site.register(Currencies)
admin.site.register(PLN_ExchangeRate)

