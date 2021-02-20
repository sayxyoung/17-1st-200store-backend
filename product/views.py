import json

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models      import MatchingReview, Review
from order.models import Order

class ReviewView(View):
    def get(self, request, product_id):
        data = json.loads(request.body)

        reviews = Review.objects.filter(product_id=product_id)
        reviews = [{
            'user'       : review.user.account,
            'content'    : review.content,
            'starRating' : review.star_rating,
            'imageUrl'  : review.image_url,
            'createAt'  : review.create_at
        } for review in reviews]

        return JsonResponse({'message':'SUCCUSS', 'date': reviews}, status=200)

    def post(self, request):
        data = json.loads(request.body)

        try:
            product_id = data['productId']
            order_id   = data['orderId']

            check_matching = MatchingReview.objects.filter(product_id=product_id, order_id=order_id)
            if check_matching.exists():
                return JsonResponse({'message':'ALREADY_HAVE_ITEM'}, status=400)
            
            with transaction.atomic():
                review = Review.objects.create(
                    product_id  = product_id,
                    user_id     = data['userId'],
                    content     = data['content'],
                    star_rating = data['starRating'],
                    image_url   = data['imageUrl'] if data.get('image_url') else 'none'
                )

                MatchingReview.objects.create(
                    review     = review,
                    order_id   = order_id,
                    product_id = product_id
                ).save()

                review.save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
