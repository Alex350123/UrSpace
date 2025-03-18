from rentals.models import Location
import pandas as pd
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load location data from an Excel file'

    def handle(self, *args, **options):
        # Path to your Excel file
        file_path = 'tables/Locations.xlsx'

        # Read the Excel file
        df = pd.read_excel(file_path)

        # Iterate over the rows of the DataFrame
        for _, row in df.iterrows():
            # Create and save the Location instance
            location = Location(
                locationname=row['Location Name'],
                longitude=row['Longitude'],
                latitude=row['Latitude'],
                locationaddress=row['Location Address']

            )
            location.save()

        # Output completion message
        self.stdout.write(self.style.SUCCESS('Successfully loaded location data into the database.'))

