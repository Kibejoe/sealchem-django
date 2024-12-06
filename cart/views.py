from django.shortcuts import render, redirect, get_object_or_404
from  store.models import Product
from .models import Cart, CartItem
from store.models import Variation
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart


#Incrementing and adding cart items

def add_cart(request, product_id):

    current_user = request.user
    product = Product.objects.get(id=product_id) # get the product

    if current_user.is_authenticated:

        product_variation = []
        if request.method == 'POST':

            for key in request.POST: 
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact = value)
                    product_variation.append(variation)
                except:
                    pass

        #Get cart item

        cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            #Existing Variations 
            #Current variation -> Check if the current variation is inside the exiting variations. If so then we increase the quantity
            #cart item id

            existing_variation_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variation.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)


            if product_variation in existing_variation_list:
                #Increase cart item quantity
                index = existing_variation_list.index(product_variation) #if product variation exists in existing variations find index of that variation in the existing variations
                item_id = id[index] #associate the variation with the index
                item = CartItem.objects.get(product=product, id=item_id) #increase quantity if it exists
                item.quantity+=1
                item.save()

            else:
                #create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=current_user) #if it does not exist create it with a quantity of 1

                if len(product_variation) > 0: # if product variation has something
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
            
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user
            )

            if len(product_variation) > 0: # if product variation has something
                cart_item.variation.clear()

                cart_item.variation.add(*product_variation) #add that to the variation field in the cart item

                    
            cart_item.save()
        return redirect('cart')


    # if user is not authenticated
    else: 
        product_variation = []
        if request.method == 'POST':

            for key in request.POST: 
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact = value)
                    product_variation.append(variation)
                except:
                    pass


        # Get cart
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #get cart using cart id present in the session

        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        
        cart.save()

        #Get cart item

        cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            #Existing Variations 
            #Current variation -> Check if the current variation is inside the exiting variations. If so then we increase the quantity
            #cart item id

            existing_variation_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variation.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)


            if product_variation in existing_variation_list:
                #Increase cart item quantity
                index = existing_variation_list.index(product_variation) #if product variation exists in existing variations find index of that variation in the existing variations
                item_id = id[index] #associate the variation with the index
                item = CartItem.objects.get(product=product, id=item_id) #increase quantity if it exists
                item.quantity+=1
                item.save()

            else:
                #create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart) #if it does not exist create it with a quantity of 1

                if len(product_variation) > 0: # if product variation has something
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
            
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )

            if len(product_variation) > 0: # if product variation has something
                cart_item.variation.clear()

                cart_item.variation.add(*product_variation) #add that to the variation field in the cart item

                    
            cart_item.save()
        return redirect('cart')

#Decrementing and removing cart items

def decrement_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:

        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')



def remove_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)

    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True) #Bring all the cart items in the actual cart

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) #Bring all the cart items in the actual cart

        for cart_item in cart_items:

            prices = cart_item.variation.values_list('price', flat=True)

            for price in prices:
                if price is not None:
                    total += price * cart_item.quantity  # Add the price multiplied by the quantity to total
                    quantity += cart_item.quantity

        tax = (4 * total)/100
        grand_total = total + tax
            
    except Cart.DoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):

    try:
        tax=0
        grand_total = 0
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True) #Bring all the cart items in the actual cart

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) #Bring all the cart items in the actual cart

        for cart_item in cart_items:
            prices = cart_item.variation.values_list('price', flat=True)

            for price in prices:
                if price is not None:
                    total += price * cart_item.quantity  # Add the price multiplied by the quantity to total
                    quantity += cart_item.quantity

        tax = (4 * total)/100
        grand_total = total + tax
            
    except Cart.DoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request,'store/checkout.html', context)