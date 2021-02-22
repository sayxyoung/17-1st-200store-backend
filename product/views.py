import json
from datetime            import datetime, timedelta

from django.http         import JsonResponse
from django.views        import View
from django.db.models    import Q
from django.utils        import timezone

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

def is_new(create_at, compare_date):
    return True if create_at > compare_date else False

def check_best_list():
    best_query = Product.objects.all().order_by('total_sales')[:10]
    return [best.id for best in best_query]

def is_best(checkList, id):
    return True if id in checkList else False 

def is_sale(sale):
    return True if sale > 0 else False

class ProductListView(View):
    def get(self, request, category_id):
        
        print(category_id)
        sorting = request.GET.get('sorting', None)
        print(sorting)

        best_list = check_best_list()
        compare_date = timezone.localtime() - timedelta(days=30)

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
                    'isNew'         : is_new(item.create_at, compare_date),
                    'isBest'        : is_best(best_list, item.id),
                    'isSale'        : is_sale(item.sale)
                }for item in product_list] 

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
                    'createAt'       : review.create_at,
                    'userId'         : review.user_id, 
            } for review in reviews]

        return JsonResponse({'message' : 'SUCCESS',
                             'data' : {
                                 'product'  : product_view,
                                 'Images'   : product_images,
                                 'review'   : product_reviews,
                            }}, status=200)


