from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import *


def Store(request):

    storeData = cartData(request)
    cartItems = storeData['cartItems']

    products = Product.objects.all
    data = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', data)


def Cart(request):

    cartDatas = cartData(request)
    cartItems = cartDatas['cartItems']
    order = cartDatas['order']
    items = cartDatas['items']

    data = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', data)


def Checkout(request):
    CheckoutData = cartData(request)
    cartItems = CheckoutData['cartItems']
    order = CheckoutData['order']
    items = CheckoutData['items']
    data = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', data)


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        Customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            Customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
        order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            Customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment complete!', safe=False)
