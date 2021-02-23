import json

import django.views import View
import django.http  import JsonResponse

import user.models  import User, RecentlyView, UserCoupon, Point
import utils        import login_decorator


class MypageMainView(View):
    RECENTLY_VIEW_COUNT = 4

    @login_decorator
    def get(self, request):
        user = request.user
        coupon = Coupon.objects.filter(user=user).count()
        point  = Point.objects.filter(user=user).order_by('-create_at')[:1]     

        # 진행 중인 주문에 대한 값들 고민하기
        # status = Order.objects.filter(user=user)
        # wating_deposit = status

        recently_views = RecentlyView.objects.filter(user=user).order_by('-create_at').distinct()[:RECENTLY_VIEW_COUNT]
        recently_views = [{
            'name'     : view.product.name,
            'imageUrl' : view.product.image_url,
            'id'       : view.product.id
        } for view in recently_views]

        return JsonResponse({
            'message'      :'SUCCESS', 
            'user'         : {
                'name'     : user.name,
                'grade'    : user.grade.name,
                'coupon'   : coupon,
                'point'    : point[0].remaining_point,
            } ,
            'orderStatus'  : {
                ''
            },
            'recentlyView' : recently_views
            }, status=200)


