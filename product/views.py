import json
from datetime     import datetime, timedelta
from pytz         import utc

from django.views import View
from django.http  import JsonResponse

from .models      import Product # image_url 추가하면 구성해주기
from order.models import Order

def is_new(create_at, compare_date):
    return True if compare_date < create_at  else False

def check_bestList():
    best_query = Product.objects.all().only('id').order_by('-total_sales')[:20]
    return [best.id for best in best_query]

def is_best(checkList, id):
    return True if id in checkList else False 

def is_sale(sale):
    return True if sale > 0 else False

class MainView(View):
    def get(self, request):
        compare_date = utc.localize(datetime.utcnow()) + timedelta(days=-30)
        checkBest    = check_bestList()

        BEST_COUNT = 4
        NEW_COUNT  = 8
        SALE_COUNT = 8

        best_query = Product.objects.all().only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at').order_by('-total_sales')[:BEST_COUNT]
        best_list  = [{
            'id'       : best.id,
            'name'     : best.name,
            'imageUrl' : best.image_url,
            'category' : best.category.id,
            'price'    : best.price,
            'sale'     : best.sale,
            'isNew'    : is_new(best.create_at, compare_date),
            'isBest'   : is_best(checkBest, best.id),
            'isSale'   : is_sale(best.sale)
        } for best in best_query]

        new_query  = Product.objects.all().only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at').order_by('-sale')[:NEW_COUNT]
        new_list   = [{
            'id'       : new.id,
            'name'     : new.name,
            'imageUrl' : new.image_url,
            'category' : new.category.id,
            'price'    : new.price,
            'sale'     : new.sale,
            'isNew'    : is_new(new.create_at, compare_date),
            'isBest'   : is_best(checkBest, new.id),
            'isSale'   : is_sale(new.sale)
        } for new in new_query]

        sale_query = Product.objects.filter(sale__gt=0).only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at')[:SALE_COUNT]
        sale_list  = [{
            'id'       : sale.id,
            'name'     : sale.name,
            'imageUrl' : sale.image_url,
            'category' : sale.category.id,
            'price'    : sale.price,
            'sale'     : sale.sale,
            'isNew'    : is_new(sale.create_at, compare_date),
            'isBest'   : is_best(checkBest, sale.id),
            'isSale'   : is_sale(sale.sale)
        } for sale in sale_query]

        return JsonResponse({
            'message' : 'SUCCESS',
            'data'    : {
                'best' : best_list,
                'new'  : new_list,
                'sale' : sale_list 
            }}, status=200)