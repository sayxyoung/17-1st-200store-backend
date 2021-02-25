import json
import uuid
from json             import JSONDecodeError

from django.db        import transaction
from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View

from order.models     import Cart
from order.models     import Order
from order.models     import OrderStatus
from product.models   import Product
from user.models      import Address
from user.models      import User
from user.views       import login_decorator

SHOPPING_BASKET = "장바구니"

class PaymentView(View):
    @login_decorator
    def get(self, request, *args, **kwargs):
        try:
            user         = request.user
            order        = Order.objects.get(user=user, status__name=SHOPPING_BASKET)
            cart_lists   = order.cart_set.all()
            product_info = [
                {
                    "cartId"    : cart_list.id,
                    "productId" : cart_list.product_id,
                    "product"   : cart_list.product.name,
                    'option'    : cart_list.option,
                    'quantity'  : cart_list.quantity,
                    'totalPrice': cart_list.total_price,
                    'eachPrice' : int(cart_list.total_price/cart_list.quantity),
                    'urlImage'  : cart_list.product.image_url,
                } for cart_list in cart_lists
            ]
            user_info = [
                {
                    'userName'       : user.name,
                    'userHomeAddress': user.home_address,
                    'userHomePhone'  : user.home_phone,
                    'userCellPhone'  : user.cell_phone,
                    'userEmail'      : user.email,
                }
            ]
            user_address_info = [
                {
                    'toPerson' : user.name,
                    'toAddress': user.home_address,
                    'homePhone': user.home_phone,
                    'cellPhone': user.cell_phone,
                }
            ]
            return JsonResponse({
                'message': 'SUCCESS',
                'result' : {
                    'product_info'     : product_info,
                    'user_info'        : user_info,
                    'user_address_info': user_address_info,
                }
            }, status=200)

        except Address.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except Order.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except Order.MultipleObjectsReturned:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except OrderStatus.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)