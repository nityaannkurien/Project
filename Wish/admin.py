from django.contrib import admin
from .models import List
from .models import ListItem
from .models import ItemDetails
# Register your models here.


admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(ItemDetails)