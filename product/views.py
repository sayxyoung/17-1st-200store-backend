import json
import datetime          as dt
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

#from user.models        import User
#from utile              import login_decorator

class ProductView(View):
    def get(self, request, category_id, sorting):
        #sorting = request.GET.get('sorting', None)
        print(category_id)

        result = []

        if category_id == 0:
            products = Product.objects.all()
            datetime_now = dt.datetime.today()
            result = [
                {
                    'name'          : products[i].name,
                    'price'         : products[i].price,
                    'sale'          : products[i].sale,
                    'image_url'     : products[i].image_url,
                    'category'      : products[i].category,
                   # 'product_likes' : products[i].
                }for i in range(len(products))] 
            if sorting == 'IsNew':
                result.order_by('create_at')
            #elif sorting == 'IsBest':
             #   result.order_by(

#            print(result)

        else:
            products = Product.objects.filter(category_id = category_id)
            result = [
                {
                    'name'          : products[i].name,
                    'price'         : products[i].price,
                    'sale'          : products[i].sale,
                    'image_url'     : products[i].image_url,
                }for i in range(len(products))]
            print(result)

        return JsonResponse({'message' : 'SUCCESS'}, status=200)


#class ProductDetailView(View):
#    def get(self, requset):
#        data = Json.loads(request.body)
#
#        product = data['name']
#
#        if Product.objects.get(id = product.id).exists()
#           
            
