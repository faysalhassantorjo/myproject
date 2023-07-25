import json
from . models import *
def cartData(request):
    cartItems=None
    order=None
    items=None
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        customer, created = Customer.objects.get_or_create(user=user,
                                                           defaults={'name': user.username, 'email': user.email})
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    return {'cartItems':cartItems,'order':order,'items':items}