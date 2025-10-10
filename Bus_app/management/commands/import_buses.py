import csv
import random
from django.core.management.base import BaseCommand
from Bus_app.models import Bus_Model, Route

class Command(BaseCommand):
    help = '/home/user/Downloads/bus_route_details/bus.txt'  #"Import buses from a txt file into Bus_Model"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to bus_routes_int_busno.txt file')

    def handle(self, *args, **options):
        path = options['file_path']

        routes = list(Route.objects.all())
        if not routes:
            self.stdout.write(self.style.ERROR("No routes found in database. Please add routes first."))
            return

        count = 0
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        bus_no = str(row[0])
                        operator_name = row[1]
                        bus_type = row[2]
                        total_seat = int(row[3])
                        price = float(row[4])

                        # Assign a random Route_Fk
                        route_fk = random.choice(routes)

                        # Set available seats equal to total seats initially
                        available_seates = total_seat

                        Bus_Model.objects.update_or_create(
                            Bus_No=bus_no,
                            defaults={
                                'Operator_name': operator_name,
                                'Bus_Types': bus_type,
                                'Total_seat': total_seat,
                                'Price': price,
                                'available_seates': available_seates,
                                'Route_Fk': route_fk,
                                # Bus_image will use default if not provided
                            }
                        )
                        count += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Skipping row due to error: {e}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {path}"))
            return

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {count} buses successfully!"))
