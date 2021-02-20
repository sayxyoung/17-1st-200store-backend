import json

from django.views import View
from django.http  import JsonResponse

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

