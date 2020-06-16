from products.models import Product

def get_products(season, filter):
    season_products = Product.objects.filter(product_colors__season=season.lower(
    )).prefetch_related('product_colors').distinct().order_by(filter)[:3]
    col_prod = []
    for product in season_products:
        colour = product.product_colors.filter(season=season.lower()).last()
        col_prod.append((product, colour))
    return col_prod
