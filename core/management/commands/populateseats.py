from django.core.management.base import BaseCommand
from core.models import Seat

class Command(BaseCommand):
    help = 'Populate seats A1–J10'

    def handle(self, *args, **kwargs):
        Seat.objects.all().delete()
        for row in [chr(i) for i in range(ord('A'), ord('J') + 1)]:
            for number in range(1, 11):
                Seat.objects.create(row=row, number=number)
        self.stdout.write(self.style.SUCCESS('Seats populated.'))
