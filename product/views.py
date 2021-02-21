import json
from datetime            import datetime, timedelta
from pytz                import utc

from django.http         import JsonResponse
from django.views        import View
from django.db.models    import Q

from .models import (
        Product,
        Category,
        ProductImage,
        ProductOption,
        ProductLike,
        Review,
        ReviewStatus,
        ProductInquiry,
        AnswerStatus,
)

def isNew(create_at, compare_date):
    return True if create_at > compare_date else False

def checkBestList():
    best_query = Product.objects.all().order_by('-total_sales')[:10]
    return [best.id for best in best_query]
    product_list = Product.objects.all().order_by('total_sales')[:10] \
        if category_id == 0 else Product.objects.filter(category_id=\
        category_id).order_by(sorting)

def isBest(checkList, id):
    return True if id in checkList else False 

def isSale(sale):
    return True if sale > 0 else False


class ProductListView(View):
    def get(self, request, **kwargs):

        best_list = checkBestList()
        category_id = kwargs['category_id']
        compare_date = utc.localize(datetime.utcnow()) - timedelta(days=30)

        if kwargs.get('sorting'):
            sorting = kwargs['sorting']
            if kwargs['sorting'] == 'isBest':
                sorting = '\'-total_sales\''
            elif kwargs['sorting'] == 'isNew':
                sorting = '-create_at'
            elif kwargs['sorting'] == 'isNew':
                sorting = '\'-sale\''
            elif kwargs['sorting'] == 'isLowPrice':
                sorting = '\'price\''
            elif kwargs['sorting'] == 'isHighPrice':
                sorting = '\'-price\''
        else :
            sorting = '-total_sales'

        product_list = Product.objects.all().order_by(sorting) \
            if category_id == 0 else Product.objects.filter(category_id=\
            category_id).order_by(sorting)
        
        products = [
                {
                    'id'            : item.id,
                    'name'          : item.name,
                    'price'         : item.price,
                    'sale'          : item.sale,
                    'stock'         : item.stock,
                    'imageUrl'      : item.image_url,
                    'category'      : item.category.id,
                    'isNew'         : isNew(item.create_at, compare_date),
                    'isBest'        : isBest(best_list, item.id),
                    'isSale'        : isSale(item.sale)
                }for item in product_list] 

        print(products)

        return JsonResponse({'message' : 'SUCCESS'}, status=200)


class ProductDetailView(View):
    def get(self, request, product_id):

        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'message' : 'DOSE_NOT_EXISTS_PRODUCT'}, status=401)

        product = Product.objects.get(id = product_id)
        reviews = Review.objects.filter(product_id = product_id)
        images  = ProductImage.objects.filter(product_id = product_id)
        inquirys = ProductInquiry.objects.filter(product_id = product_id)

        product_view = [
            {
                    'id'             : product.id,
                    'name'           : product.name,
                    'price'          : product.price,
                    'sale'           : product.sale,
                    'stock'          : product.stock,
                    'imageUrl'       : product.image_url,
            }]
        product_images = [
            {
                    'id'             : image.id,
                    'imageUrl'       : image.image_url,
            } for image in images]
        product_reviews = [
            {
                    'id'             : review.id,
                    'content'        : review.content,
                    'starRating'     : review.star_rating,
#                    'imageUrl'       : review.image_url,
                    'createAt'       : review.create_at,
                    'userId'         : review.user_id, 
            } for review in reviews]
#        product_inquirys = [
#            {
#                    'id'             : inquiry.id,
#                    'title'          : inquiry.title,
#                    'content'        : inquiry.content,
#                    'answerTitle'    : inquiry.answer_title,
#                    'answerContent'  : inquiry.answer_content,
#                    'createAt'       : inquiry.create_at,
#                    'answerStatusId' : inquiry.answer_status_id,
#                    'productId'      : inquiry.product_id,
#                    'user_id'        : inquiry.user_id,
#            } for inquiry in inquirys]
#         
        return JsonResponse({'message' : 'SUCCESS',
                             'data' : {
                                 'product'  : product_view,
                                 'Images'   : product_images,
                                 'review'   : product_reviews,
#                                 'inquirts' : product_inquirys
                            }}, status=200)


