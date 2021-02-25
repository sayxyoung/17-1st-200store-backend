import json
from datetime       import datetime, timedelta

from django.http    import JsonResponse
from django.views   import View
from django.utils   import timezone

from order.models   import Order, Cart
from product.models import MatchingReview
from utils          import login_decorator

class OrderListView(View):
    @login_decorator
    def get(self, request):
        compare_date = timezone.localtime() - timedelta(days=7)
        start_date   = request.GET.get('startDate', compare_date)
        end_date     = request.GET.get('endDate', timezone.localtime())

        orders = Order.objects.filter(user_id=request.user.id, create_at__range=(start_date, end_date))
        
        result = [{
            'serialNumber' : order.serial_number,
            'orderStatus'  : order.status.id,
            'orderDate'    : order.create_at,
            'orderId'      : order.id,
            'subProducts'  : [{
                'id'            : cart.product.id,
                'name'          : cart.product.name,
                'totalPrice'    : cart.total_price,
                'quantity'      : cart.quantity,
                'productStatus' : cart.status.id,
                'isReview'      : MatchingReview.objects.filter(order=order.id, product=cart.product).exists()
            } for cart in Cart.objects.filter(order_id=order.id)]
        } for order in orders]

        return JsonResponse({'message':'SUCCESS', 'data': result}, status=200)

    @login_decorator
    def patch(self, request):
        data = json.loads(request.body)

        try:
            # status_type = reqeust.GET.get('statusType', None)
            status_id  = request.GET.get('statusId', None)
            order_id   = data['orderId']
            product_id = data['productId'] 

            product           = Cart.objects.get(order_id=order_id, product_id=product_id)
            product.status_id = status_id
            product.save()

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXIST'}, status=400)
        
        return JsonResponse({'message':'SUCCESS'}, status=200)