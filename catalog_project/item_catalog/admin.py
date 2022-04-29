from django.contrib import admin
from .models import Item, Comment, Rating

admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Rating)