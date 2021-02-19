from datetime import datetime
from datetime import timedelta
from json     import JSONDecodeError
from jwt      import DecodeError

import bcrypt
import json
import jwt
import re

from django.http import JsonResponse
from django.views import View

from my_settings import ALGORITHM
from my_settings import SECRET_KEY
from user.models import Coupon
from user.models import Grade
from user.models import User
from user.models import UserCoupon

CELL_PHONE_EXPRESSION = re.compile('^[0-9]{3}\-?[0-9]{4}\-?[0-9]{4}$')
PASSWORD_EXPRESSION   = re.compile('^(?=.*[a-z])(?=.*[A-z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,16}$')
EMAIL_EXPRESSION      = re.compile('^[^-_.]*[0-9]+[@]{1}[a-zA-Z0-9]+[.]{1}[a-zA-Z]{2,3}$')

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            account      = data.get('account', None)
            password     = data.get('password', None)
            name         = data.get('name', None)
            email        = data.get('email', None)
            cell_phone   = data.get('cell_phone', None)
            home_phone   = data.get('home_phone', None)
            home_address = data.get('home_address', None)
            phone_spam   = data.get('phone_spam', False)
            email_spam   = data.get('email_spam', False)

            if not (account and password and name and email and cell_phone):
                return JsonResponse({'message': 'BadRequest'}, status=400)

            if not PASSWORD_EXPRESSION.search(password):
                return JsonResponse({'message': 'InvalidPassword'}, status=400)

            if not EMAIL_EXPRESSION.search(email):
                return JsonResponse({'message': 'InvalidEmail'}, status=400)

            if not CELL_PHONE_EXPRESSION.search(cell_phone):
                return JsonResponse({'message': 'InvalidCellphone'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')

            initial_grade = Grade.objects.get(id=1)
            user = User.objects.create(
                account    = account,
                password   = decoded_hashed_password,
                name       = name,
                email      = email,
                cell_phone = cell_phone,
                home_phone = home_phone,
                phone_spam = phone_spam,
                email_spam = email_spam,
                grade      = initial_grade,
            )
            coupon = Coupon.objects.get(id=1)
            welcome_coupon_validity = user.create_at + timedelta(days=30)
            user_coupon = UserCoupon.objects.create(
                user_id   = user.id,
                coupon_id = coupon.id,
                validity  = welcome_coupon_validity,
            )

            return JsonResponse({'message': 'Success'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BadRequest'}, status=400)