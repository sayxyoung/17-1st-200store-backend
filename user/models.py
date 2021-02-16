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
    address         = models.CharField(max_length=300, null=True)
    phone_spam      = models.SmallIntegerField(default=0)
    email_spam      = models.SmallIntegerField(default=0)
    grade           = models.ForeignKey('grades', on_delete=models.CASCADE)
    coupon          = models.ManyToManyField('coupon', through='usercoupons')
    products        = models.ManyToManyField('product.products', through='recentlyview')
    create_at       = models.DateTimeField(auto_now_add=True)
    update_at       = models.DateTimeField(auto_add=True)

    def __str__(self):
        return f'{self.user_name}'

    class Meta:
        db_table = 'users'

# 등급
class Grade(models.Model):
    name            = models.CharField(max_length=20)
    total_amount    = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'grades'

# 적립금
class Point(models.Model):
    user        = models.ForeignKey('users', on_delete=models.CASCADE)
    content     = models.CharField(max_length=50)
    validity    = models.DateTimeField()
    is_used     = models.SmallIntegerField()
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
    user        = models.ForeignKey('users', on_delete=models.CASCADE)
    coupon      = models.ForeignKey('coupons', on_delete=models.CASCADE)
    validity    = models.DateTimeField() 
    create_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usercoupons'

# 배송지
class Destination(models.Model):
    user        = models.ForeignKey('users', on_delete=models.CASCADE)
    name        = models.CharField(max_length=20)
    to_person   = models.CharField(max_length=20)
    to_address  = models.CharField(max_length=300)
    home_phone  = models.CharField(max_length=20)
    cell_phone  = models.CharField(max_length=20)
    is_default  = models.SmallIntegerField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'destinations'

# 최근 본 상품
class RecentlyView(models.Model):
    user        = models.ForeignKey('users', on_delete=models.CASCADE)
    product     = models.ForeignKey('product.products', on_delete=models.CASCADE)
    create_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recentlyview'


