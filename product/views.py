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
        ProductLike,
        Review,
        ReviewStatus,
)

def is_new(create_at, compare_date):
    return create_at > compare_date 

def check_best_list():
    best_query = Product.objects.all().order_by('total_sales')[:10]
    return [best.id for best in best_query]

def is_best(checkList, id):
    return id in checkList 

def is_sale(sale):
    return sale > 0 

class ProductListView(View):
    def get(self, request):
        category_name   = request.GET.get('category', None)
        sorting         = request.GET.get('sorting', '-total_sales')
        best_list       = check_best_list()
        compare_date    = timezone.localtime() - timedelta(days=30)

        product_list = Product.objects.all().order_by(sorting) \
            if category_name is None else Product.objects.filter(category__name =\
            category_name).order_by(sorting)

        products = [
               {
                    'id'         : item.id,
                    'name'       : item.name,
                    'price'      : item.price,
                    'sale'       : item.sale,
                    'stock'      : item.stock,
                    'imageUrl'   : item.image_url,
                    'category'   : item.category.id,
                    'isNew'      : is_new(item.create_at, compare_date),
                    'isBest'     : is_best(best_list, item.id),
                    'isSale'     : is_sale(item.sale)
                }for item in product_list] 

        return JsonResponse({'data' : {'products' : products,}}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'message' : 'PRODUCT_DOSE_NOT_EXISTS'}, status=404)
        
        product = Product.objects.get(id = product_id)
        reviews = product.review_set.all()
        images  = product.productimage_set.all()

        product_view = {
                    'id'        : product.id,
                    'name'      : product.name,
                    'price'     : product.price,
                    'sale'      : product.sale,
                    'stock'     : product.stock,
                    'imageUrl'  : product.image_url,
                    'imageUrls' : [image.image_url for image in images]
            }
        product_reviews = [
            {
                    'id'        : review.id,
                    'content'   : review.content,
                    'starRating': review.star_rating,
                    'createAt'  : review.create_at,
                    'userId'    : review.user_id, 
            } for review in reviews]

        return JsonResponse({'data' : {
                                 'product'  : product_view,
                                 'review'   : product_reviews,
                            }}, status=200)

