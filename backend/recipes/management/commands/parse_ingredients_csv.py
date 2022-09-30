import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

PATH = "backend/data"


class Command(BaseCommand):
    help = "import data from ingredients.csv"

    def handle(self, *args, **kwargs):
        with open(f"{PATH}/ingredients.csv", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            ingredients_to_add = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients_to_add)
