from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.models import Product
# To relate two apps eachother
from store.admin import ProductAdmin
from tags.models import TaggedItem
# Register your models here.


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)