from django.contrib import admin
from . import models
from django.db.models.aggregates import Count
from django.db.models import F
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode

from django.urls import reverse # For get url of products page
# Register your models here.



class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('=10', 'Just'),
            ('>10', 'OK')
        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>10':
            return queryset.filter(inventory__gt=10)
        elif self.value() == '=10':
            return queryset.filter(inventory=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']  # Collection Related Object
    list_editable = ['unit_price']
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection'] # Preload and down to 7 queries instead of 17 
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory') # To make sortable
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'



#admin.site.register(models.Collection)
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')

    def products_count(self, collection):
        #reverse('admin:app_model_page')
        # 8- Providing Links to other pages
        url = (
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
        #return collection.products_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count = Count('product'))



# admin.site.register(models.Product, ProductAdmin)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith'] #Search Box

    # It's functioning but why? 
    @admin.display(ordering='orders')
    def orders(self, order):
        url = (
            reverse('admin:store_customer_changelist')
            + "?"
            + urlencode({
                'order__id': str(order.id)
            })
        )
        return format_html('<a href="{}">{}</a>',url,order.orders)
        #return customer.orders
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders = F('order__id'))

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'placed_at', 'customer']
    list_per_page = 25