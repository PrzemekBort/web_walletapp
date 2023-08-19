from django.core.management.base import BaseCommand
from main.models import PLN_ExchangeRate


class Command(BaseCommand):

    def handle(self, *args, **options):
        currencies = PLN_ExchangeRate.objects.all()
        for cur in currencies:
            print(cur)
            cur.update()
