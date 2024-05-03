# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.



class List(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,null=True, blank=True)
    
    wishlist_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=True)
    wishlist_name =  models.CharField(max_length=255)
    description =models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.wishlist_id)

class ItemDetails(models.Model):
    item_name = models.CharField(max_length=255,null=True)
    item_id = models.CharField(max_length=255,default=None)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=255,null=True, blank=True) 
   # status = models.CharField(max_length=255, null=True, blank=True)
   # link = models.URLField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)  

    def __str__(self):
        return self.item_name
    
class ListItem(models.Model):
    wishlist = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255,)
    item_id = models.ForeignKey(ItemDetails, on_delete=models.CASCADE, blank=True,default=None)

    # Add more fields if needed

    def __str__(self):
        return self.item_name

