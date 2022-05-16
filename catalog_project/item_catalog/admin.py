from django.contrib import admin
from .models import Item, Comment, Rating

# Register all to item site
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Rating)