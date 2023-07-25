from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import *
import json
from .utils import cartData
from django.contrib.auth.models import User,auth
from django.contrib import messages


def category_list(request):
    categories = Category.objects.all()
    Data = cartData(request)
    cartItems = Data['cartItems']
    items = Data['items']
    order = Data['order']
    context = {'items': items, 'order': order, 'cartItems': cartItems,'categories':categories}
    return render(request, 'myapp/Category.html',context)


def product_list(request, category_id):
    Data = cartData(request)
    cartItems = Data['cartItems']
    categories = Category.objects.all()

    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'myapp/productScreen.html',
                  {'products': products ,'cartItems':cartItems,'categories': categories})

def productDetails(request,product_id):
    product=Product.objects.get(id=product_id)
    Data = cartData(request)
    cartItems = Data['cartItems']
    categories = Category.objects.all()

    return render(request,'myapp/productDetails.html',{'product':product,'cartItems':cartItems,'categories':categories})

def cart(request):

    Data = cartData(request)
    cartItems = Data['cartItems']
    items = Data['items']
    order = Data['order']
    categories = Category.objects.all()
    context={'items':items,'order':order,'cartItems':cartItems,"categories":categories}
    return render(request,'myapp/cart.html',context)

def checkout(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    categories = Category.objects.all()
    context = {'cartItems': cartItems, 'order': order,'categories':categories}
    return render(request,'myapp/checkout.html',context)



def updatItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data['productID']
    action = data['action']

    size=data['selectedSize']
    print(size)

    user = request.user.username
    customer, created = Customer.objects.get_or_create(id=request.user.customer.id, defaults={'name': user, 'user': user})
    print("Nam: ",user)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product,size=size)
    if action == 'add':
        if product.instock == 0:
            messages.success(request,"out of stock")
        elif orderItem.quantity>=2:
                messages.info(request,"maximum order limit is 2")
        else:
            orderItem.quantity = (orderItem.quantity + 1)
            product.instock = (product.instock - 1)
            messages.success(request,"Item added successfully")
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        product.instock = (product.instock + 1)

    orderItem.save()
    product.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def updatCartItem(request):
    # data = json.loads(request.body)
    # print(data)
    # productId = data['productID']
    # action = data['action']
    # user = request.user.username
    # customer = Customer.objects.get(id=request.user.customer.id)
    # product = Product.objects.get(id=productId)
    # order= Order.objects.get(customer=customer, complete=False)
    # orderItem = OrderItem.objects.get(order=order, product=product)
    # if action == 'add':
    #     orderItem.quantity = (orderItem.quantity + 1)
    #     product.instock = (product.instock - 1)
    #     messages.success(request, "Item added successfully")
    # elif action == 'remove':
    #     orderItem.quantity = (orderItem.quantity - 1)
    #     product.instock = (product.instock + 1)
    #
    # # orderItem.save()
    # product.save()
    # if orderItem.quantity <= 0:
    #     orderItem.delete()
    return JsonResponse("Operation done", safe=False)

import datetime
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        data['form']['name'] = request.user.customer.name
        data['form']['email'] = request.user.customer.email
        transaction_id = datetime.datetime.now().timestamp()

        if request.user.is_authenticated:
            customer = request.user.customer
            address= data['shipping']['address']
            phon_number= data['shipping']['phon-number']
            total=data['form']['total']

            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            shipping,created=ShippingAddress.objects.get_or_create(customer=customer,oder=order,address=address,phonNumber=phon_number)
            shipping.save()
            total = float(data['form']['total'])
            order.transaction_id = transaction_id
            if total == order.get_cart_total:
                order.complete = True
            order.save()


            o1=Order.objects.get(customer=customer,transaction_id=transaction_id)
            a=[]
            orderItems = OrderItem.objects.filter(order=order)
            for i in orderItems:
                a.append(f'Product Name: {i.product.name} Quantity: {i.quantity} Size: {i.size}')
                a.append("\n")

            htmlstring=str(a)
            customorder = htmlstring.replace('\n', '<br>')
            print(customorder)
            name=request.user.username
            customerOrder = CustomerOrder(order_by=order,customer_name=name, shipping=shipping,total_tk=total,orderItem=customorder)
            customerOrder.save()




    total = float(data['form']['total'])
    order.transaction_id=transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    print('data',data)

    return JsonResponse('Payment complete',safe=False)

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pass']
        password2=request.POST['pass2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exist!!! User different username')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password not the same')
            return redirect('register')
    else:
        return render(request,'myapp/register.html')

def login(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        pas=request.POST['pass']
        # if User.objects.filter(username=name).exists() and User.objects.filter(password=pas):
        user=auth.authenticate(username=name,password=pas,email=email)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Password did not match')
            return redirect('login')
    else:
        return render(request,'myapp/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')