from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

def store(request, category_slug=None):
    categories = None #When there is no category slug display no categories. So when we refresh, products still show
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,  #context is the dictionary passed from the view to the template. The key used in the context will be the key to be used in the template. The value is the result of the query i.e Products.objects.all().filter()
        'product_count': product_count
    }
    
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug =category_slug, slug = product_slug) #2 underscores for getting to the slug of the model
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product
    }
    
    return render(request, 'store/product_detail.html', context)



