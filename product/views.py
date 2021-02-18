import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from django.views import View
from django.http  import JsonResponse

from .models      import Product # image_url 추가하면 구성해주기
from order.models import Order

class MainView(View):
    def get(self, request):
        bset = Product.objects.all().only('id', 'name', 'price').order_by()[:4]


        return JsonResponse({
            'message':'SUCCESS', 
            'data': {
                'best': best,
                'new' : new,
                'sale': sale 
            }
        })

# OrderStatus.objects.create(name='상품 구매중')
# Address.objects.create(user_id=1, name='집', to_person='장성준', to_address='서울시', home_phone='111', cell_phone='111', is_default=True)
# Order.objects.create(total_price=0, confirm=True, serial_number='1', status_id=1, user_id=1, address=1)
# Cart.ojbects.create(order_id=1, product_id=1, option='asd', quantity=3, total_price=3000)
# ProductLike.objects.create(user_id=1, product_id=1)