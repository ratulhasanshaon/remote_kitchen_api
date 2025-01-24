from traceback import print_exception
from django.db import models
from django.contrib.auth.models import User




class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default='/sample.jpg')
    details = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self) -> str:
        return str(self.name +'-'+ self.restaurant.name)

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    isAvailable = models.BooleanField(default=True)
    _id =  models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    vat = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    deliveryCharge = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)



class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    _id =  models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class DeliveryAddress(models.Model):
     order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
     address = models.CharField(max_length=200, null=True, blank=True)
     city = models.CharField(max_length=200, null=True, blank=True)
     postalCode =models.CharField(max_length=200, null=True, blank=True)
     country =models.CharField(max_length=200, null=True, blank=True)
     delvieryCharge = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
     _id =  models.AutoField(primary_key=True, editable=False)

     def __str__(self):
        return str(self.address)

class PaymentInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    clientSecret = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return f"Payment for Order {self.order._id}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPES = [
        ('normal', 'Normal User'),
        ('owner', 'Owner'),
        ('employee', 'Employee'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='normal')
    if user_type == 'employee':
        restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
        
    elif user_type == 'owner':
        restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    else:
        restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.email