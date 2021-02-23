import json

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction, IntegrityError

from user.models    import User
from order.models   import Order
from product.models import ProductLike, Product, MatchingReview, Review
from utils          import login_decorator

class ProductLikeView(View):
    @login_decorator
    def get(self, request):
        
        likes = ProductLike.objects.filter(user_id = request.user.id)
        likes = [{
            'id'       : like.product.id,
            'name'     : like.product.name,
            'imageUrl' : like.product.image_url,
            'category' : like.product.category.id
        } for like in likes]g

        return JsonResponse({'message':'SUCCESS', 'data':likes}, status=200)
    
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        check_have  = ProductLike.objects.get_or_create(user_id=request.user.id, product_id=data['productId'])
        have_like   = check_have[0]
        is_have_like = check_have[1]
        
        if not is_have_like: have_like.delete()

        return JsonResponse({'message':'SUCCESS'}, status=200)

class ReviewView(View):
    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        reviews = [{
            'user'       : review.user.account,
            'content'    : review.content,
            'starRating' : review.star_rating,
            'imageUrl'  : review.image_url,
            'createAt'  : review.create_at
        } for review in reviews]

        return JsonResponse({'message':'SUCCUSS', 'date': reviews}, status=200)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            product_id = int(data['productId'])
            order_id   = int(data['orderId'])

            check_matching = MatchingReview.objects.filter(product_id=product_id, order_id=order_id)
            if check_matching.exists():
                return JsonResponse({'message':'ALREADY_HAVE_ITEM'}, status=400)
            
            with transaction.atomic():
                review = Review.objects.create(
                    product_id  = product_id,
                    user_id     = request.user.id,
                    title       = data['title'],
                    content     = data['content'],
                    star_rating = data['starRating'],
                    image_url   = data['imageUrl'] if data.get('image_url') else 'none'
                )

                MatchingReview.objects.create(
                    review     = review,
                    order_id   = order_id,
                    product_id = product_id
                )

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except IntegrityError:
            return JsonResponse({'message':'INTEGERITY_ERROR'}, status=400)

        return JsonResponse({'message':'SUCCESS'}, status=200)