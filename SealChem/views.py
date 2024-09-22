from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products  #context is the dictionary passed from the view to the template. The key used in the context will be the key used in the template. The value is the result of the query i.e Products.objects.all().filter()
    }
    return render(request, 'home.html', context)