from django.shortcuts import render
from store.models import Product, ReviewRating, Variation
from django.db.models import Min, Max

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')[:10]


    product_list = []

    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
        variation_prices = Variation.objects.filter(product=product, is_active=True).aggregate(min_price=Min('price'),max_price=Max('price'))

        variation_count = Variation.objects.filter(product=product, is_active=True).count()

        # Determine if there's only one variation
        single_price = None
        if variation_count == 1:
            single_price = Variation.objects.filter(product=product, is_active=True).first().price

        data = {
            'product': product,  #context is the dictionary passed from the view to the template. The key used in the context will be the key used in the template. The value is the result of the query i.e Products.objects.all().filter()
            'reviews': reviews,
            'min_price': variation_prices['min_price'],
            'max_price': variation_prices['max_price'],
            'single_price': single_price,  # Include single price if applicable

        }

        product_list.append(data)

    context = {
        'product_list': product_list
    }
    return render(request, 'home.html', context)