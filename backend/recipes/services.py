from django.http import HttpResponse


def convert_to_file(cart_ingredients):
    """Функция для формирования списка покупок."""
    file_name = "shoppinglist.txt"
    shopping_cart = []
    for ing in cart_ingredients:
        name = ing["ingredient__name"]
        measurement_unit = ing["ingredient__measurement_unit"]
        amount = ing["ingredient_total_amount"]
        shopping_cart.append(f"{name}: {amount} {measurement_unit}")
    shopping_cart.append("\nПриятных покупок!")
    content = "\n".join(shopping_cart)
    content_type = "text/plain,charset=utf8"
    response = HttpResponse(content, content_type=content_type)
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    return response
