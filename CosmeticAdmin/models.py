from django.db import models


class Administator(models.Model):
    admin_username = models.CharField(max_length=20, unique=True)
    admin_email = models.EmailField()
    ContactNumber = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    password_confirmation = models.CharField(max_length=20)
    def __str__(self):              
        return self.admin_username

class Subadmin(models.Model):
    administator = models.ForeignKey(Administator, on_delete=models.CASCADE)    
    subadmin_username = models.CharField(max_length=20,unique=True)
    subadmin_email = models.EmailField()
    subadmin_Number = models.CharField(max_length=10)
    subadmin_password = models.CharField(max_length=255)
    subadmin_password1 = models.CharField(max_length=20)
    
    def __str__(self):
        return f'username: { self.subadmin_username } - super user: { self.administator.admin_username }'
        
class Product(models.Model):
    subadmin = models.ForeignKey(Subadmin, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    Subcategory = models.CharField(max_length=30)
    ProductName = models.CharField(max_length=64)
    ActualPrice = models.CharField(max_length=10)
    offerPrice  = models.CharField(max_length=10,null=True,blank=True)
    ProductColour = models.CharField(max_length=30)
    StackQuantity = models.IntegerField()
    DeliveryCost = models.CharField(max_length=10)
    ProductDetails = models.TextField()
    ProductInformation = models.TextField()
    HowToUse = models.TextField()
    img1 = models.FileField(upload_to='product/')
    img2 = models.FileField(upload_to='product/')
    img3 = models.FileField(upload_to='product/')
    img4 = models.FileField(upload_to='product/')
    img5 = models.FileField(upload_to='product/')
    def __str__(self):
        return f'Category: { self.category} - Subcategory: { self.Subcategory} - Admin: { self.subadmin.subadmin_username}'


        

