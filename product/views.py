import json
from datetime     import datetime, timedelta

from django.utils import timezone
from django.views import View
from django.http  import JsonResponse

from user.models    import User
from order.models   import Order
from product.models import ProductLike, Product, MatchingReview, Review
from utils          import login_decorator

def is_new(create_at, compare_date):
    return compare_date < create_at

def check_bestList():
    best_query = Product.objects.all().only('id').order_by('-total_sales')[:20]
    return [best.id for best in best_query]

def is_best(checkList, id):
    return id in checkList

def is_sale(sale):
    return sale > 0

class ProductLikeView(View):
    @login_decorator
    def get(self, request):
        
        likes = reqeust.user.productlike_set.all()
        likes = [{
            'id'       : like.product.id,
            'name'     : like.product.name,
            'imageUrl' : like.product.image_url,
            'category' : like.product.category.id
        } for like in likes]

        return JsonResponse({'message':'SUCCESS', 'data':likes}, status=200)
    
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        have_like, is_have_like = ProductLike.objects.get_or_create(user_id=request.user.id, product_id=data['productId'])
        if not is_have_like: have_like.delete()

        return JsonResponse({'message':'SUCCESS'}, status=200)

class MainView(View):
    def get(self, request):
        compare_date = compare_date = timezone.localtime() - timedelta(days=30) + timedelta(days=-30)
        checkBest    = check_bestList()

        BEST_COUNT = 4
        NEW_COUNT  = 8
        SALE_COUNT = 8

        best_query = Product.objects.all().order_by('-total_sales')[:BEST_COUNT]
        best_list  = [{
            'id'       : best.id,
            'name'     : best.name,
            'imageUrl' : best.image_url,
            'category' : best.category.id,
            'price'    : best.price,
            'sale'     : best.sale,
            'isNew'    : is_new(best.create_at, compare_date),
            'isBest'   : is_best(checkBest, best.id),
            'isSale'   : is_sale(best.sale)
        } for best in best_query]

        new_query  = Product.objects.all().order_by('-sale')[:NEW_COUNT]
        new_list   = [{
            'id'       : new.id,
            'name'     : new.name,
            'imageUrl' : new.image_url,
            'category' : new.category.id,
            'price'    : new.price,
            'sale'     : new.sale,
            'isNew'    : is_new(new.create_at, compare_date),
            'isBest'   : is_best(checkBest, new.id),
            'isSale'   : is_sale(new.sale)
        } for new in new_query]

        sale_query = Product.objects.filter(sale__gt=0)[:SALE_COUNT]
        sale_list  = [{
            'id'       : sale.id,
            'name'     : sale.name,
            'imageUrl' : sale.image_url,
            'category' : sale.category.id,
            'price'    : sale.price,
            'sale'     : sale.sale,
            'isNew'    : is_new(sale.create_at, compare_date),
            'isBest'   : is_best(checkBest, sale.id),
            'isSale'   : is_sale(sale.sale)
        } for sale in sale_query]

        return JsonResponse({
            'message' : 'SUCCESS',
            'data'    : {
                'best' : best_list,
                'new'  : new_list,
                'sale' : sale_list 
            }}, status=200)

class ReviewView(View):
    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        reviews = [{
            'user'       : review.user.account,
            'content'    : review.content,
            'starRating' : review.star_rating,
            'imageUrl'   : review.image_url,
            'createAt'   : review.create_at
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