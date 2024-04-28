# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class List(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,null=True, blank=True)
    wishlist_name =  models.CharField(max_length=255)
    wishlist_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=True)
    description =models.TextField(null=True,blank=True)

    def __str__(self):
        return self.wishlist_name
    
class ListItem(models.Model):
    wishlist = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    status = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='wishlists/', null=True, blank=True)  


    # Add more fields if needed 

    def __str__(self):
        return self.item_name