from django.db import models

# 주문
class Order(models.Model):
    user        = models.ForeignKey('user.users', on_delete=models.CASCADE)
    product     = models.ForeignKey('product.products', on_delete=models.CASCADE)
    status      = models.ForeignKey('statuses', on_delete=models.CASCADE)
    product     = models.ManyToManyField('product.products', through='cart.carts')
    create_at   = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    confirm     = models.SmallIntegerField()

    class Meta:
        db_table = 'orders'

# 주문 상태
class OrderStatus(models.Model):
    name        = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'orderstatuses'
