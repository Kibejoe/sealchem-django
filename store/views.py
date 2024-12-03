from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductGallery, Variation
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from django.db.models import Min, Max


def store(request, category_slug=None):
    categories = None #When there is no category slug display no categories. So when we refresh, products still show

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,  #context is the dictionary passed from the view to the template. The key used in the context will be the key to be used in the template. The value is the result of the query i.e Products.objects.all().filter()
        'product_count': product_count
        
    }
    
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug =category_slug, slug = product_slug) #2 underscores for getting to the slug of the model
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id= single_product.id).exists()

        except OrderProduct.DoesNotExist :
            orderproduct = None
    
    else:
        orderproduct= None


    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    #Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id = single_product.id)

    variation_prices = Variation.objects.filter(product=single_product, is_active=True).aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )

    variation_count = Variation.objects.filter(product=single_product, is_active=True).count()

    # Determine if there's only one variation
    single_price = None
    if variation_count == 1:
        single_price = Variation.objects.filter(product=single_product, is_active=True).first().price


    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,        
        'min_price': variation_prices['min_price'],
        'max_price': variation_prices['max_price'],
        'single_price': single_price
    }
    
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains = keyword))
            product_count = products.count()
        context = {
            'products': products,
            'product_count': product_count
        }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id = product_id)
            form = ReviewForm(request.POST, instance=reviews) #instance creates a new updated review
            form.save()
            messages.success(request, 'Thank you, your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)

            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                
                data.save()  

                messages.success(request, 'Thanks your review is submitted')
                return redirect(url)



