from handler.models import Movies, Genre, Links
import csv

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Choose a movieset to load into database'
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('dataset',
                            choices=['1m', '25m', 'small'],
                            type=str,
                            )

    def handle(self, *args, **options):
        # ...
        if options['delete']:
            poll.delete()
        # ...
