from datetime           import datetime, timedelta
from json               import JSONDecodeError
from jwt                import DecodeError

import bcrypt, json, jwt, re, pandas

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Count

from my_settings        import ALGORITHM, SECRET_KEY
from user.models        import Coupon, Grade, User, UserCoupon, RecentlyView, Point
from order.models       import Order, OrderStatus
from utils              import login_decorator

CELL_PHONE_EXPRESSION = re.compile('^[0-9]{3}\-?[0-9]{4}\-?[0-9]{4}$')
EMAIL_EXPRESSION      = re.compile('^[^-_.]*[0-9]+[@]{1}[a-zA-Z0-9]+[.]{1}[a-zA-Z]{2,3}$')
PASSWORD_EXPRESSION   = re.compile('^(?=.*[a-z])(?=.*[A-z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,16}$')

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            account  = data['account']
            password = data['password']

            if not User.objects.filter(account=account).exists():
                return JsonResponse({'message': 'INVALID_USER_ID'}, status=401)

            user                    = User.objects.get(account=account)
            decoded_hashed_password = user.password

            if not bcrypt.checkpw(password.encode('utf-8'), decoded_hashed_password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

            access_token = jwt.encode({'userPk': user.pk}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'accessToken': access_token}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

class SignUpView(View):
    def post(self, request):
        GENERAL_MEMBER_GROUP = "일반회원그룹"
        WELCOME_COUPON       = "웰컴 쿠폰"

        try:
            data         = json.loads(request.body)
            account      = data['account']
            password     = data['password']
            name         = data['name']
            email        = data['email']
            cell_phone   = data['cellPhone']
            home_phone   = data.get('homePhone', None)
            home_address = data.get('homeAddress', None)
            phone_spam   = data.get('phoneSpam', False)
            email_spam   = data.get('emailSpam', False)

            if not PASSWORD_EXPRESSION.search(password):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

            if not EMAIL_EXPRESSION.search(email):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

            if not CELL_PHONE_EXPRESSION.search(cell_phone):
                return JsonResponse({'message': 'INVALID_CELLPHONE'}, status=400)

            hashed_password         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')
            initial_grade = Grade.objects.get(name=GENERAL_MEMBER_GROUP)
            user = User.objects.create(
                account      = account,
                password     = decoded_hashed_password,
                name         = name,
                email        = email,
                cell_phone   = cell_phone,
                home_phone   = home_phone,
                home_address = home_address,
                phone_spam   = phone_spam,
                email_spam   = email_spam,
                grade        = initial_grade,
            )
            UserCoupon.objects.create(
                user_id  = user.id,
                coupon   = Coupon.objects.get(name=WELCOME_COUPON),
                validity = user.create_at + timedelta(days=30),
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'BAD_REQUEST'},status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'})

class MyPageMainView(View):
    @login_decorator
    def get(self, request):
        RECENTLY_VIEW_COUNT = 4 

        user         = request.user
        coupon       = Coupon.objects.filter(user=user).count()
        point        = Point.objects.filter(user=user).order_by('-create_at').first()
        orders       = Order.objects.filter(user_id=user.id).values('status__name').annotate(count=Count('status')) 

        recently_views = RecentlyView.objects.filter(user=user).\
                order_by('-create_at').distinct()[:RECENTLY_VIEW_COUNT]

        recently_views = [{
            'name'     : view.product.name,
            'imageUrl' : view.product.image_url,
            'id'       : view.product.id
        } for view in recently_views]

        return JsonResponse({
                'user'     : {
                'name'     : user.name,
                'grade'    : user.grade.name,
                'coupon'   : coupon,
                'point'    : point.remaining_point,
            },
            'orderStatus'  : [{
                        'name'     : order['status__name'], 
                        'count'    : order['count'] 
            } for order in orders],
            'recentlyView' : recently_views
        })
