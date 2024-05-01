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

    def _str_(self):
        return str(self.wishlist_id)
    
    
class ListItem(models.Model):
    wishlist= models.ForeignKey(List, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255,null=True)
    
    # Add more fields if needed 

    def _str_(self):
        return self.item_name