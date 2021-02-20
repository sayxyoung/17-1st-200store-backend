import json
from datetime            import datetime, timedelta

from django.http         import JsonResponse
from django.views        import View
#from django.db.models    import Q

from .models import (
        Product,
        Category,
)

def IsNew(products):
    datetime_now = datetime.today() - timedelta(days=30)
    return [products for item in products if item.create_at < datetime_now]

def IsBest(products):
    return products.order_by('total_sales')

def IsSale(products):
    return [products for item in products if item.sale > 0]

def IsLowPrice(products):
    return products.order_by('-price')

def IsHighPrice(products):
    return products.order_by('price')


class ProductListView(View):
    def get(self, request, **kwargs):

        category_id = kwargs['category_id']

        product_list = Product.objects.all().only('name').order_by('-total_sales') \
        if category_id == 0 else Product.objects.filter(category_id=\
        category_id).only('name').order_by('-total_sales')
        
        products = [
                {
                    'id'            : item.id,
                    'name'          : item.name,
                    'price'         : item.price,
                    'sale'          : item.sale,
                    'imageUrl'      : item.image_url,
                    'category'      : item.category,
                    'createAt'      : item.create_at,
                    'totalSales'    : item.total_sales,
                }for item in product_list] 
#        print(products)
#        if kwargs['sorting']:
#            sorting = kwargs['sorting']
#            if sorting == 'isNew':
#                new = IsNew(products)
#            elif sorting == 'isBest':
#                best = IsBest(products) 
#            elif sorting == 'isSale':
#                best = IsSale(products) 
#            elif sorting == 'isLowPrice':
#                lowprice = IsLowPrice(products)
#            elif sorting == 'isHighPrice':
#                highprice = IsHighPrice(products)
#            else :
#                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
#
        return JsonResponse({'message' : 'SUCCESS'}, status=200)

class ProductDetailView(View):
    def get(self, request):
        return JsonResponse({'message' : 'SUCCESS'}, status=200)


