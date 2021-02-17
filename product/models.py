from django.db import models

# 상품
class Product(models.Model):
    category        = models.ForeignKey('category', on_delete=models.CASCADE)
    name            = models.CharField(max_length=50)
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    stock           = models.PositiveIntegerField(default=0)
    sale            = models.DecimalField(max_digits=5, decimal_places=3,default=0)
    user            = models.ManyToManyField('user.user', through='productlike',related_name='product_like')
    create_at       = models.DateTimeField(auto_now_add=True)
    update_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'products'

# 카테고리
class Category(models.Model):
    name            = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'categories'

# 상품 이미지
class ProductImage(models.Model):
    product         = models.ForeignKey('product', on_delete=models.CASCADE)
    image_url       = models.URLField(max_length=4000)

    class Meta:
        db_table = 'product_images'

# 상품 좋아요
class ProductLike(models.Model):
    product         = models.ForeignKey('product', on_delete=models.CASCADE)
    user            = models.ForeignKey('user.user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_likes'

class ProductOption(models.Model):
    product         = models.ForeignKey('product', on_delete=models.CASCADE)
    name            = models.CharField(max_length=100)
    stock           = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'product_options'

# 상품 리뷰
class Review(models.Model):
    product         = models.ForeignKey('product', on_delete=models.CASCADE)
    user            = models.ForeignKey('user.user', on_delete=models.CASCADE)
    content         = models.CharField(max_length=4000)
    star_rating     = models.SmallIntegerField()
    image_url       = models.URLField(max_length=4000)
    create_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'

# 상품 상태 중간테이블
class ReviewStatus(models.Model):
    review          = models.ForeignKey('product', on_delete=models.CASCADE)
    order           = models.ForeignKey('order.order', on_delete=models.CASCADE)

    class Mets:
        db_table = 'review_statuses'


# 상품 문의
class ProductInquiry(models.Model):
    product         = models.ForeignKey('product', on_delete=models.CASCADE)
    user            = models.ForeignKey('user.user', on_delete=models.CASCADE)
    title           = models.CharField(max_length=50)
    content         = models.CharField(max_length=4000)
    answer_title    = models.CharField(max_length=50)
    answer_content  = models.CharField(max_length=4000)
    answer_status   = models.ForeignKey('answerstatus', on_delete=models.CASCADE)
    create_at       = models.DateTimeField(auto_now_add=True)

    class Mete:
        db_table = 'product_inquiries'

# 질문답변 상태
class AnswerStatus(models.Model):
    name            = models.CharField(max_length=20)

    class Meta:
        db_table = 'answer_statuses'

