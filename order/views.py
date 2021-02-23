import json

from django.http    import JsonResponse
from django.views   import View

from order.models   import Order, Cart
from product.models import MatchingReview

class OrderListView(View):
    def get(self, request):
        data   = json.loads(request.body)
        orders = Order.objects.filter(user_id=data['userId']) # decorator 되면 거기서 받아오기
        
        order_list = []

        for order in orders:
            carts = Cart.objects.filter(order_id=order.id)
            sub_products = [
                
                {
                'id'            : cart.product.id,
                'name'          : cart.product.name,
                'totalPrice'    : cart.total_price,
                'quantity'      : cart.quantity,
                'productStatus' : 2,  # cart.status (구매확정)
                'isReview'      : True if is_review.exists() else False
            } for cart in carts]

            insert_order = {
                'serialNumber' : order.serial_number,
                'orderStatus'  : order.status,
                'orderDate'    : order.create_at,
                'orderId'      : order.id,
                'subProducts'  : sub_products
            }
            order_list.append(insert_order)

        return JsonResponse({'message':'SUCCESS', 'data': order_list}, status=200)