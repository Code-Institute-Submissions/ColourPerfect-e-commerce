from django.shortcuts import render, get_object_or_404
from products.models import Product
# Create your views here.
def product(request, id):

    SEASONS = ['Spring', 'Summer', 'Autumn', 'Winter']
    product = get_object_or_404(Product, pk=id)
    all_colours = product.product_colors.all()
    brand = product.brand.all()
    category = product.category.all()

    colours = {}
    
    if all_colours:
        for season in SEASONS:
            season_colours = []
            for colour in all_colours:
                if colour.season == season.lower():
                    season_colours.append(colour)
            colours[season] = season_colours

    has_colours = bool(colours)

    context = {
        'product': product,
        'colours': colours,
        'brand': brand,
        'category': category,
        'seasons': SEASONS,
        'has_colours': has_colours,

    }

    return render(request, 'product.html', context)