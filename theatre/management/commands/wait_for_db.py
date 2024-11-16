import time

from django.core.management.base import BaseCommand
from django.db import connections, OperationalError

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        while True:
            try:
                connections["default"].ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database available!"))
                break
            except OperationalError as e:
                self.stdout.write(f"Database unavailable, waiting 1 second... ({e})")
                time.sleep(1)
