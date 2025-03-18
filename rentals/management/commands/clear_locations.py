from django.core.management.base import BaseCommand
from rentals.models import Location

class Command(BaseCommand):
    help = 'Deletes all vehicle data.'

    def handle(self, *args, **options):
        Location.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All location data has been successfully deleted.'))
