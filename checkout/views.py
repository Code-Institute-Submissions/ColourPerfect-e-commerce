import stripe
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from checkout.forms import OrderForm
from basket.models import BasketItem, Basket
from basket.contexts import basket_content
from checkout.models import Order, OrderItem
from products.models import Product, Colour


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        

        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['first_name'],
            'email_address': request.POST['email_address'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        current_basket = basket_content(request)
        total = current_basket['total']
        order_form = OrderForm(form_data)
        
        if order_form.is_valid():
            order = order_form.save()
            order.total = total
            order.save()

            if request.user.is_authenticated:
                
                basket_items = BasketItem.objects.filter(basket__owner=request.user)
                for basket_item in basket_items:
                    order_item = OrderItem(order=order, product=basket_item.product, quantity=basket_item.quantity, colour=basket_item.colour)
                    order_item.save()
                
            else: 
                basket = request.session.get('basket', {})

                for item in basket:
                    product = Product.objects.get(pk=basket[item]['product'])
                    quantity = basket[item]['quantity']
                    colour = None
                    if Colour.objects.filter(pk=basket[item]['colour']).exists():
                        colour = Colour.objects.get(pk=basket[item]['colour'])

                    order_item = OrderItem(order=order, product=product, quantity=quantity, colour=colour)
                    order_item.save()

            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There is an error in your form, please check your data')
   
    else:

        if request.user.is_authenticated:
            if BasketItem.objects.filter(basket__owner=request.user).exists():
                basket = Basket.objects.get(owner=request.user)
            else:
                basket = None
        else: 
            basket = request.session.get('basket', {})

        if not basket:
            messages.error(request, "There's nothing in your basket at the moment")
            return redirect(reverse('basket'))

        current_basket = basket_content(request)
        total = current_basket['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            )


    order_form = OrderForm()
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout.html', context)

def checkout_success(request, order_number):
    
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Success - all the fabulous colours are on their way to you! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email_address}.')

    if request.user.is_authenticated and BasketItem.objects.filter(basket__owner=request.user).exists():

        BasketItem.objects.filter(basket__owner=request.user).delete()

    elif 'basket' in request.session:

        del request.session['basket']

    context = {
        'order': order,
    }

    return render(request, 'checkout-success.html', context)   