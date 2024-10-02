from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from .forms import ShippingAddress_Form

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
    order = Order.objects.get()
    # items = order.orderitem_set.all()
    context = {"items": items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    if request.method == 'POST':
        form = ShippingAddress_Form(request.POST, request.FILES)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.customer = customer
            shipping_address.order = order
            shipping_address.save()

            form.save()
    form = ShippingAddress_Form()

    order = Order.objects.get()
    items = order.orderitem_set.all()
    context = {"items": items, 'order': order, 'form': form}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    # Проверяем, что запрос является POST-запросом
    if request.method == 'POST':
        # Получаем данные из тела запроса
        data = json.loads(request.body)  # Используем request.body вместо request.data
        productId = data['productId']
        action = data['action']

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            OrderItem.quantity -= 1
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()
        return JsonResponse('item was added', safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
