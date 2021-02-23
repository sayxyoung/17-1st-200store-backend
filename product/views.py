import json

from django.views import View
from django.http  import JsonResponse

from user.models import User
from .models     import ProductLike, Product

class ProductLikeView(View):
    def get(self, request, user_id):
        
        # user_id -> login decorator를 받아서 하기
        likes = ProductLike.objects.filter(user_id = user_id)
        likes = [{
            'id'       : like.product.id,
            'name'     : like.product.name,
            'imageUrl' : like.product.image_url,
            'category' : like.product.category.id
        } for like in likes]g

        return JsonResponse({'message':'SUCCESS', 'data':likes}, status=200)
    
    def post(self, request):
        data = json.loads(request.body)

        check_have  = ProductLike.objects.get_or_create(user_id=data['userId'], product_id=data['productId'])
        have_like   = check_have[0]
        is_have_like = check_have[1]
        
        if not is_have_like: have_like.delete()

        return JsonResponse({'message':'SUCCESS'}, status=200)