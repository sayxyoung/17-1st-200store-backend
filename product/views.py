import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from datetime from datetime, timedelta

from django.views import View
from django.http  import JsonResponse

from .models      import Product # image_url 추가하면 구성해주기
from order.models import Order

def isNew(create_at, compare_date):
    return True if create_at > compare_date else False

def checkBestList():
    best_query = Product.objects.all().only('id').order_by('-total_sales')[:20]
    return [best.id for best in best_query]

def isBest(checkList, id):
    return True if id in checkList else False 

def isSale(sale):
    return True if sale > 0 else False

class MainView(View):
    def get(self, request):
        compare_date = datetime.today() + datetime.timedelta(days=-30)
        checkBest    = checkBestList()

        best_query = Product.objects.all().only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at').order_by('-total_sales')[:4]
        best_list  = [{
            'id'       : best.id,
            'name'     : best.name,
            'imageUrl' : best.image_url,
            'category' : bset.category_id,
            'price'    : best.price,
            'sale'     : best.sale,
            'isNew'    : isNew(best.create_at, compare_date),
            'isBest'   : isBest(checkBestList, best.id),
            'isSale'   : isSale(best.sale)
        } for best in best_query]

        new_query  = Product.objects.all().only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at').order_by('-sale')[:8]
        new_list   = [{
            'id'       : new.id,
            'name'     : new.name,
            'imageUrl' : new.image_url,
            'category' : new.category_id,
            'price'    : new.price,
            'sale'     : new.sale,
            'isNew'    : isNew(best.create_at, compare_date),
            'isBest'   : isBest(checkBestList, new.id),
            'isSale'   : isSale(new.sale)
        } for new in new_query]

        sale_query = Product.objects.filter(sale__gt=0).only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at')[:8]
        sale_list  = [{
            'id'       : sale.id,
            'name'     : sale.name,
            'imageUrl' : sale.image_url,
            'category' : sale.category_id,
            'price'    : sale.price,
            'sale'     : sale.sale,
            'isNew'    : isNew(best.create_at, compare_date),
            'isBest'   : isBest(checkBestList, sale.id),
            'isSale'   : isSale(sale.sale)
        } for sale in sale_query]

        return JsonResponse({
            'message'  : 'SUCCESS',
            'status'   : 200 
            'data'     : {
                'best' : best_list,
                'new'  : new_list,
                'sale' : sale_list 
            }
        })