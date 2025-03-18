from django.core.management.base import BaseCommand
from rentals.models import Room, Location
import pandas as pd

class Command(BaseCommand):
    help = 'Load rooms from database'
    def handle(self, *args, **options):
        file_path = 'tables/Rooms.xlsx'
        # Read the Excel file
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            # Create and save the Location instance
            location_instance = Location.objects.get(Locationid=row['Locationid'])
            room = Room(
                Locationid=location_instance,
                roomtype=row['roomtype'],
                availability=row['availability'],
                price =row['price'],
                is_defective_wifi= row['is_defective_wifi'],
                is_defective_chair= row['is_defective_chair'],
                is_detective_light= row['is_defective_light'],
                is_defective_socket= row['is_defective_socket'],

            )
            room.save()

        # Output completion message
        self.stdout.write(self.style.SUCCESS('Successfully loaded location data into the database.'))

