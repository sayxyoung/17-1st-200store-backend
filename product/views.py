import json
from datetime            import datetime, timedelta

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

def IsNew(products):
    datetime_now = dt.datetime.today() - timedelta(days=30)
    return [products for item in products if item.create_at < datetime_now]

def IsBest(products):
    return products.order_by('total_sales')

def IsSale(products):
    return [products for item in products if item.sale > 0]

def IsLowPrice(products):
    return products.order_by('-price')

def IsHighPrice(products):
    return products.order_by('price')


class ProductListView(View):
    def get(self, request, **kwargs):

        category_id = kwargs['category_id']

        product_list = Product.objects.all().only('name').order_by('-total_sales') \
        if category_id == 0 else Product.objects.filter(category_id=\
        category_id).only('name').order_by('-total_sales')
        
        products = [
                {
                    'id'            : item.id,
                    'name'          : item.name,
                    'price'         : item.price,
                    'sale'          : item.sale,
                    'stock'         : item.stock,
                    'imageUrl'      : item.image_url,
                    'category'      : item.category,
                    'createAt'      : item.create_at,
                    'totalSales'    : item.total_sales,
                }for item in product_list] 

#        print(products)
#        if kwargs['sorting']:
#            sorting = kwargs['sorting']
#            if sorting == 'isNew':
#                new = IsNew(products)
#            elif sorting == 'isBest':
#                best = IsBest(products) 
#            elif sorting == 'isSale':
#                best = IsSale(products) 
#            elif sorting == 'isLowPrice':
#                lowprice = IsLowPrice(products)
#            elif sorting == 'isHighPrice':
#                highprice = IsHighPrice(products)
#            else :
#                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
#
        return JsonResponse({'message' : 'SUCCESS',
                             'data' : product_list},
                             status=200)


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
                            }})

















            
