from django.db import models
from CosmeticAdmin.models import *

class Customer(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50, blank=True)  
    username = models.CharField(max_length=128, unique=True)
    PhoneNumber = models.CharField(max_length=10)
    CustomerEmail = models.EmailField()
    CustomerPassword = models.CharField(max_length=50)
    ConfirmPassword = models.CharField(max_length=50)
def __str__(self):              
    return self.username

class Cart(models.Model):
    Product=models.ForeignKey(Product, on_delete=models.CASCADE)    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cart_price=models.BigIntegerField(default=0)
    
    def __str__(self):
        return f'Product Category: {self.Product.Subcategory} - Product Name: {self.Product.ProductName}'

class Orders(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)    
    retailer=models.ForeignKey(Subadmin,on_delete=models.SET_NULL,null=True,blank=True)
    delivery_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    quantity = models.PositiveIntegerField(default=0, null=True,blank=True)
    cart_price=models.BigIntegerField(default=0,null=True,blank=True)