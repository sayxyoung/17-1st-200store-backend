from django.db import models
from django.db.models.fields.related import ForeignKey

# 유저
class User(models.Model):
    user_id         = models.CharField(max_length=20)
    user_password   = models.CharField(max_length=300)
    user_name       = models.CharField(max_length=20)
    email           = models.EmailField(max_length=50)
    cell_phone      = models.CharField(max_length=20)
    home_phone      = models.CharField(max_length=20, null=True)
    user_address    = models.CharField(max_length=300, null=True)
    phone_spam      = models.BooleanField(default=False)
    email_spam      = models.BooleanField(default=False)
    grade           = models.ForeignKey('grade', on_delete=models.CASCADE)
    coupon          = models.ManyToManyField('coupon', through='usercoupon')
    product         = models.ManyToManyField('product.product', through='recentlyview', related_name='recently_view')
    create_at       = models.DateTimeField(auto_now_add=True)
    update_at       = models.DateTimeField(auto_now=True)
    total_price     = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user_name}'

    class Meta:
        db_table = 'users'

# 등급
class Grade(models.Model):
    name            = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'grades'

# 적립금
class Point(models.Model):
    user        = models.ForeignKey('user', on_delete=models.CASCADE)
    content     = models.CharField(max_length=50)
    validity    = models.DateTimeField()
    is_used     = models.BooleanField(default=False)
    create_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content}'

    class Meta:
        db_table = 'points'

# 쿠폰
class Coupon(models.Model):
    name        = models.CharField(max_length=30)
    price       = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'coupons'

# 유저 쿠폰 (중간테이블)
class UserCoupon(models.Model):
    user        = models.ForeignKey('user', on_delete=models.CASCADE)
    coupon      = models.ForeignKey('coupon', on_delete=models.CASCADE)
    validity    = models.DateTimeField() 
    create_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_coupons'

# 배송지
class address(models.Model):
    user        = models.ForeignKey('user', on_delete=models.CASCADE)
    name        = models.CharField(max_length=20)
    to_person   = models.CharField(max_length=20)
    to_address  = models.CharField(max_length=300)
    home_phone  = models.CharField(max_length=20)
    cell_phone  = models.CharField(max_length=20)
    is_default  = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'addresses'

# 최근 본 상품
class RecentlyView(models.Model):
    user        = models.ForeignKey('user', on_delete=models.CASCADE)
    product     = models.ForeignKey('product.product', on_delete=models.CASCADE)
    create_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recently_views'


