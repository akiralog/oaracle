from django.core.management.base import BaseCommand
from conditions.models import ThamesTown


class Command(BaseCommand):
    help = 'Populate ThamesTown database with Chiswick and Putney'

    def handle(self, *args, **options):
        # Your working data from the Python script
        towns_data = [
            {
                'town_name': 'Chiswick',
                'location_id': 304120,
                'is_tidal': True
            },
            {
                'town_name': 'Putney',
                'location_id': 304117,
                'is_tidal': True
            }
        ]

        created_count = 0
        updated_count = 0

        for town_data in towns_data:
            town, created = ThamesTown.objects.get_or_create(
                location_id=town_data['location_id'],
                defaults={
                    'town_name': town_data['town_name'],
                    'is_tidal': town_data['is_tidal']
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {town.town_name} (ID: {town.location_id}, Tidal: {town.is_tidal})')
                )
            else:
                # Update existing record
                town.town_name = town_data['town_name']
                town.is_tidal = town_data['is_tidal']
                town.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated: {town.town_name} (ID: {town.location_id}, Tidal: {town.is_tidal})')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Done! Created: {created_count}, Updated: {updated_count}')
        )
