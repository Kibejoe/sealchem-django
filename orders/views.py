from datetime import date
from django.shortcuts import render, redirect
from cart.models import CartItem
from store.models import Product
from .forms import OrderForm
from .models import Order, OrderProduct
from django.urls import reverse

#Verification email

from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def place_order(request, quantity=0, total=0):
    current_user = request.user

    # if cart_count <=0 redirect to store

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <=0:
        return redirect('store')
    
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        prices = cart_item.variation.values_list('price', flat=True)
        for price in prices:
            if price is not None:
                total += price * cart_item.quantity
                quantity += cart_item.quantity

    tax = (2*total)/100
    grand_total = total+tax 
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #Store billing information
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.order_total = grand_total
            data.tax= tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()


            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            cart_items = CartItem.objects.filter(user=current_user)
            for item in cart_items:
                order_product = OrderProduct()
                order_product.order_id = order.id
                order_product.user_id = order.user.id
                order_product.product_id = item.product_id
                order_product.quantity = item.quantity
                order_product.ordered = True
                # Assign product price
                prices = item.variation.values_list('price', flat=True)
                for price in prices:
                    if price is not None:
                        order_product.product_price = price

                order_product.save()

                # Assign product variations
                product_variation = item.variation.all()
                order_product.variation.set(product_variation)
                order_product.save()

                # Reduce product stock
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

                
            CartItem.objects.filter(user=order.user).delete()

                        # Mark the order as completed
            order.is_ordered = True
            order.save()

            # Send order confirmation email
            mail_subject = 'Thank you for placing an order with us'
            message = render_to_string('orders/order_received_email.html', {
                'user': order.user,
                'order': order,
            })
            to_email = order.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()


            return redirect(f"{reverse('order_complete')}?order_number={order_number}")
        
    return redirect('checkout')
        

def order_complete(request):
    order_number = request.GET.get('order_number')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)

        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity


        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Order.DoesNotExist):
        return redirect('home')
    



