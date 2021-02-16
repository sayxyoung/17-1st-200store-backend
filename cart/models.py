from django.db import models

# 장바구니
class Cart(models.Model):
    order       = models.ForeignKey('order.orders', on_delete=models.CASCADE)
    product     = models.ForeignKey('product.products', on_delete=models.CASCADE)
    option      = models.CharField(max_length=100)
    count       = models.SmallIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'carts'
