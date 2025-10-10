import csv
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from Bus_app.models import Route

class Command(BaseCommand):
    help = '/home/user/Downloads/bus_route_details/routes_details.txt'  #  'Import routes from a txt file (no header required)'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to routes.txt file')

    def handle(self, *args, **options):
        path = options['file_path']
        count = 0

        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)  # simple reader, no header
                for row in reader:
                    try:
                        # Each row: source,destination,departure_time,arrival_time,Available_date
                        source, destination, dep_str, arr_str, date_str = row

                        # Parse times
                        dep_time = datetime.strptime(dep_str, "%H:%M").time()
                        arr_time = datetime.strptime(arr_str, "%H:%M").time()

                        # Calculate duration
                        dep_dt = datetime.combine(datetime.today(), dep_time)
                        arr_dt = datetime.combine(datetime.today(), arr_time)
                        if arr_dt < dep_dt:
                            arr_dt += timedelta(days=1)
                        duration = arr_dt - dep_dt

                        # Parse available date
                        available_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                        # Update or create the route
                        Route.objects.update_or_create(
                            source=source,
                            destination=destination,
                            Available_date=available_date,
                            defaults={
                                'departure_time': dep_time,
                                'arrival_time': arr_time,
                                'duration': duration,
                            }
                        )
                        count += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Skipping row due to error: {e}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {path}"))
            return

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {count} routes successfully!"))
