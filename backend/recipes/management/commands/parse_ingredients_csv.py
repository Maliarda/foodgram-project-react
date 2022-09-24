import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient

PATH = "backend/data"


class Command(BaseCommand):
    help = "import data from category.csv"

    def handle(self, *args, **kwargs):
        with open(f"{PATH}/ingredients.csv", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                print(row)

                ingredient = Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                ingredient.save()
