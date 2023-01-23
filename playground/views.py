from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order, Customer
# Create your views here.


def say_hello(request):
    return HttpResponse("Hello!")  # Should be mapped in urls.py


def index(request):
    # return render(request, 'index.html', {"name": 'Django'})
    return render(request, 'index.html',{'name': 'Django'})



from django.db import transaction

# @transaction.atomic()
def orm_test(request):
    #query_set = Product.objects.all()
    # print(query_set[0:5])

    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass

    # product = Product.objects.filter(pk=0).first()  # Better than try except

    # # To check ezxistance of this record True/False
    # exists = Product.objects.filter(pk=0).exists()

    # query_set = Product.objects.filter(unit_price=20)  # if uinit_price = 20
    # query_set = Product.objects.filter(
    #     unit_price__gt=20)  # if uinit_price > 20

    # query_set = Product.objects.filter(unit_price__range=(20, 30))

    #query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # query_set = Product.objects.filter(
    #    Q(inventory__lt=10) | Q(unit_price__lt=20))
    # query_set = Product.objects.filter(
    #     inventory=F('unit_price'))  # To compare two col

    # Sorting
    #query_set = Product.objects.order_by('unit_price', '-title').reverse()

    # Limitig Results
    # query_set = Product.objects.order_by('-title')[:5]
    #query_set = Product.objects.order_by('-title')[5:10] 
    """
        SELECT `store_product`.`id`,
        `store_product`.`title`,
        `store_product`.`slug`,
        `store_product`.`description`,
        `store_product`.`unit_price`,
        `store_product`.`inventory`,
        `store_product`.`last_update`,
        `store_product`.`collection_id`
        FROM `store_product`
        ORDER BY `store_product`.`title` DESC
        LIMIT 5
        OFFSET 5
    """
    # Selecting Fields to Query
    #query_set = Product.objects.values_list('id', 'title', 'collection__title')
    """
        SELECT `store_product`.`id`,
        `store_product`.`title`,
        `store_collection`.`title`
        FROM `store_product`
        INNER JOIN `store_collection`
        ON (`store_product`.`collection_id` = `store_collection`.`id`)
    """
    #query_set = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')
    #query_set = Product.objects.only('id', 'title') # Look to queries when render Unit_Price
    #query_set = Product.objects.defer('description') # Select All except Description*
    
    # select_related (1)
    # prefetch_related (n)

    #query_set = Product.objects.select_related('collection').all()
    #query_set = Product.objects.prefetch_related('promotion').all()
    #query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    
    #query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').all().order_by('-placed_at')[:5]
    
    #return render(request, 'index.html', {'name': 'Django', 'orders': list(query_set)})

    # Aggregate
    # from django.db.models.aggregates import Count, Min, Max, Avg, Sum

    # result = OrderItem.objects.filter(product__id=1).aggregate(units_sold=Sum('quantity'))
    
    # return render(request, 'index.html', {'name': 'Django', 'result': result})
    
    #Annotating
    # from django.db.models import Value, F, Func
    # query_set = Customer.objects.annotate(is_new=Value(True))

    # Calling Database Function
    # query_set = Customer.objects.annotate(full_name = Func(F('first_name'), Value(' '),F('last_name'), function='CONCAT'))
    # from django.db.models.functions import Concat
    # query_set = Customer.objects.annotate(full_name = Concat(F('first_name'), Value(' '),F('last_name')))
    # from django.db.models import Count

    # #query_set = Customer.objects.annotate(orders_count=Count('order'))

    # #Expression Wrapper
    # #query_set = Product.objects.annotate(discount_price = F('unit_price') * 0.8) #Cannot infer type of '*' expression involving these types: DecimalField, FloatField. You must set output_field.
    # # from django.db.models import ExpressionWrapper, DecimalField
    # # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # # query_set = Product.objects.annotate(discounted_price=discounted_price) 
    # # return render(request, 'index.html', {'name': 'Django', 'result': list(query_set)})

    # #Querying Generic Relationships
    # from django.contrib.contenttypes.models import ContentType
    # from store.models import Product
    # from tags.models import TaggedItem

    # # content_type = ContentType.objects.get_for_model(Product)
    # # query_set = TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=1)

    # query_set = TaggedItem.objects.get_tags_for(Product, 1)  # Exact same as above but we just encapsulate it

    # return render(request, 'index.html', {'name': 'Django', 'result': list(query_set)})

    # #Cache
    # query_set = Product.objects.all()
    # list(query_set)
    # query_set[0] #Use cache
    # Use 3 Queries 

    # query_set = Product.objects.all()
    # query_set[0] #Don't Use cache, Use a query 
    # list(query_set)
    # Use 4 Queries 


    #Insert INTO 

    from store.models import Collection
    # # Creating Objects
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()


    # Update 
    # collection = Collection(pk=11)
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()
    
    # If we dont set title here, we will have a problem so we have to first get pk then update field.
 
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()

    # Collection.objects.filter(pk=11).update(featured_product=None)

    # Delete 
    # collection = Collection(pk=11)
    # collection.delete() # All Collection

    #Collection.objects.filter(id__gt=5).delete()
    


    #Transaction 

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()


    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    query_set = Product.objects.raw('SELECT * FROM store_product')

    return render(request, 'index.html', {'name': 'Django', 'result': list(query_set)})
