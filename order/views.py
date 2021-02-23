import json
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
from utils            import login_decorator

SHOPPING_BASKET = "장바구니"
class CartView(View):
    @login_decorator
    def post(self, request, *args, **kwargs):
        try:
            data       = json.loads(request.body)
            user       = request.user
            productId  = data['productId']
            totalPrice = data['totalPrice']
            quantity   = data['quantity']
            product    = Product.objects.get(id=productId)

            if not Address.objects.filter(user=user, is_default=True).exists():
                user_to_address = user.home_address
                if not user_to_address:
                    user_to_address = ''

                address = Address.objects.create(
                    user       = user,
                    name       = user.name,
                    to_person  = user.name,
                    to_address = user_to_address,
                    cell_phone = user.cell_phone,
                    is_default = True,
                )

            order_status = OrderStatus.objects.get(name=SHOPPING_BASKET)
            if not Order.objects.filter(user=user, status=order_status).exists():
                address = Address.objects.filter(user=user, is_default=True)
                Order.objects.create(
                    user          = user,
                    status        = order_status,
                    address       = address[0],
                    total_price   = 0,
                    serial_number = '추가구현예정',
                )

            order = Order.objects.get(user=user, status=order_status)
            if not Cart.objects.filter(order=order, product=product).exists():
                Cart.objects.create(
                    order       = order,
                    product     = product,
                    option      = '',
                    quantity    = quantity,
                    total_price = int(totalPrice),
                )
            else:
                cart              = Cart.objects.get(order=order, product=product)
                cart.quantity    += int(quantity)
                cart.total_price += int(totalPrice)
                cart.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

    @login_decorator
    def get(self, request, *args, **kwargs):
        try:
            user         = request.user
            order_status = OrderStatus.objects.get(name=SHOPPING_BASKET)
            order        = Order.objects.get(user=user, status=order_status)
            cart_lists   = Cart.objects.filter(order=order)
            result = [
                {
                    'productId' : cart_list.product_id,
                    'product'   : cart_list.product.name,
                    'option'    : cart_list.option,
                    'quantity'  : cart_list.quantity,
                    'totalPrice': int(cart_list.total_price),
                    'eachPrice' : int(cart_list.total_price/cart_list.quantity),
                    'urlImage'  : cart_list.product.image_url,
                } for cart_list in cart_lists
            ]
            return JsonResponse({'message': 'SUCCESS', 'result': result}, status=200)

        except Order.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

    @login_decorator
    def delete(self, request, *args, **kwargs):
        try:
            user                  = request.user
            data                  = json.loads(request.body)
            product_list          = data['product']
            delete_productId_list = [product_list[idx]['productId'] for idx in range(len(product_list))]
            order_status          = OrderStatus.objects.get(name=CartView.SHOPPING_BASKET)
            order                 = Order.objects.get(user=user, status=order_status)
            cart                  = Cart.objects.filter(order=order, product_id__in=delete_productId_list)
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