import json
import uuid
from json             import JSONDecodeError
from datetime         import datetime, timedelta

from django.db        import transaction
from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View
from django.utils     import timezone

from order.models     import Order, Cart, OrderStatus
from product.models   import MatchingReview
from user.models      import Address, User
from utils            import login_decorator

SHOPPING_BASKET = "장바구니"

class CartView(View):
    @login_decorator
    def post(self, request, *args, **kwargs):
        try:
            data         = json.loads(request.body)
            user         = request.user
            product_id   = data['productId']
            total_price  = data['totalPrice']
            quantity     = data['quantity']
            order_status = OrderStatus.objects.get(name=SHOPPING_BASKET)

            if not Order.objects.filter(user=user, status=order_status).exists():
                order = Order.objects.create(
                    user          = user,
                    status        = order_status,
                    serial_number = str(uuid.uuid4())
                )
                Cart.objects.create(
                    order       = order,
                    product_id  = product_id,
                    quantity    = quantity,
                    total_price = int(total_price),
                )
                return JsonResponse({'message': 'SUCCESS'}, status=200)

            order = Order.objects.get(user=user, status=order_status)
            if not Cart.objects.filter(order=order, product_id=product_id).exists():
                Cart.objects.create(
                    order       = order,
                    product_id  = product_id,
                    quantity    = quantity,
                    total_price = int(total_price),
                )
                return JsonResponse({'message': 'SUCCESS'}, status=200)

            cart              = Cart.objects.get(order=order, product_id=product_id)
            cart.quantity    += int(quantity)
            cart.total_price += int(total_price)
            cart.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except Order.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except Order.MultipleObjectsReturned:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

    @login_decorator
    def get(self, request, *args, **kwargs):
        try:
            user         = request.user
            order        = Order.objects.get(user=user, status__name=SHOPPING_BASKET)
            cart_lists   = order.cart_set.all()
            result = [
                {
                    'cartId'    : cart_list.id,
                    'productId' : cart_list.product_id,
                    'product'   : cart_list.product.name,
                    'option'    : cart_list.option,
                    'quantity'  : cart_list.quantity,
                    'totalPrice': int(cart_list.total_price),
                    'eachPrice' : cart_list.product.price,
                    'urlImage'  : cart_list.product.image_url,
                } for cart_list in cart_lists
            ]
            return JsonResponse({'message': 'SUCCESS', 'result': result}, status=200)

        except Order.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

    @login_decorator
    def delete(self, request, *args, **kwargs):
        try:
            cart_id_list = request.GET.getlist('cartId', None)
            int_cart_id  = [int(cart_id) for cart_id in cart_id_list]
            cart         = Cart.objects.filter(id__in=int_cart_id)
            if not cart.exists():
                return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

            cart.delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except Order.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except OrderStatus.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

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
            } for cart in order.cart_set.all()]
        } for order in orders]

        return JsonResponse({'message':'SUCCESS', 'data': result}, status=200)

    @login_decorator
    def patch(self, request):
        data = json.loads(request.body)

        try:
            order_id   = data['orderId']
            product_id = data['productId'] 

            product           = Cart.objects.get(order_id=order_id, product_id=product_id)
            product.status_id = 4
            product.save()

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXIST'}, status=400)
        
        return JsonResponse({'message':'SUCCESS'}, status=200)
