import json

from django.views import View
from django.http  import JsonResponse

from user.models import User
from .models     import ProductLike, Product

class ProductLikeView(View):
    def get(self, request, user_id):
        
        products = ProductLike.objects.filter(user_id = user_id)
        products = [{
            'id'       : product.product.id,
            'name'     : product.product.name,
            'imageUrl' : product.product.image_url
        } for product in products]

        # print(products)

        return JsonResponse({'message':'SUCCESS', 'status' : 200, 'data'   : products
        })
    
    def post(self, request):
        data = json.loads(request.body)

        check_have = ProductLike.objects.get_or_create(user_id=data['userId'], product_id=data['productId'])
        if not check_have[1]: check_have[0].delete()

        # 뿌리는것 까지 하기!

        return JsonResponse({'message':'SUCCESS', 'status' : 200})