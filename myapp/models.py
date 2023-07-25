from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#
#     image = models.ImageField(null=True, blank=True)
#
#     def __str__(self):
#         return str(self.name)
#
#     @property
#     def imageURL(self):
#         try:
#             url = self.image.url
#         except:
#             url = ''
#         return url


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description=models.CharField(default="",max_length=200)
    image = models.ImageField(null=True, blank=True)

    price = models.IntegerField(default=0)
    instock=models.IntegerField(default=0)
    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(default=datetime.now, db_index=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.customer.name)

    @property
    def shipping(self):
        shipping = False
        return shipping

    @property
    def get_cart_total(self):
        orederitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orederitems)
        return total

    @property
    def get_cart_items(self):
        orederitems = self.orderitem_set.all()
        total = sum(item.quantity for item in orederitems)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    date_added=models.DateTimeField(default=datetime.now)
    size=models.CharField(max_length=10)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def productnameandquantity(self):
        name = self.product.name
        qty = str(self.quantity)
        return 'ProductName:' + name + ' Quntity:' + qty + '   '


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    oder = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100)
    phonNumber = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.address


class CustomerOrder(models.Model):
    order_by = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    customer_name=models.CharField(max_length=100)
    shipping = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    orderItem = models.TextField()
    total_tk=models.CharField(max_length=100)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Order No: {self.id}'