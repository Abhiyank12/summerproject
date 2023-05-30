from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from .validators import CustomUniqueValidationError


# Create your models here.
class Carousel(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = HTMLField(default=False)
    image = models.FileField(null=True, blank=True)
    def __str__(self):
        return self.title

class category(models.Model):
    name = models.CharField(max_length=100, unique=True,error_messages={'unique':'Custom unique constraint failed.'})
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, null=False, blank=False, default=False)
    name = models.CharField(max_length=200, null=False, blank=False,default=False)
    description = HTMLField()
    image = models.FileField(null=False, blank=False,default=False)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price =models.CharField(max_length=100, null=False, blank=False,default=False)
    mfgdate =models.DateTimeField(default=timezone.now)
    expdate = models.DateTimeField(null=True,blank=True)
    costperpro = models.CharField(max_length=100,null=True,blank=True,default=False)
    def __str__(self):
        return self.name
    
    
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,default=False)
    phoneno=models.CharField(max_length=10,null=False,blank=False,unique=True)
    address=models.CharField(max_length=100,null=False,blank=False)
    def __str__(self):
        return self.user
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.TextField(default={'objects': []}, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    

ORDERSTATUS = ((1, "Pending"), (2, "Dispatch"), (3, "On the way"), (4, "Delivered"), (5, "Cancel"), (6, "Return"))
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.TextField(default={'objects': []}, null=True, blank=True)
    total = models.CharField(max_length=100,null=False,blank=True)
    status = models.IntegerField(choices=ORDERSTATUS,default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
METHOD=(("cash on deliver","cash on delivery"),
        ("esewa","esewa"))
class payment(models.Model):
    payment_method= models.CharField(max_length=100, choices= METHOD, default="Cash on delivery")
    payment_created= models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.payment_method