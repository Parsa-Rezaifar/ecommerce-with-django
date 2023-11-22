from django.db import models
from django.contrib.auth import get_user_model
from Home.models import Product
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

class Order(models.Model) :

    user = models.ForeignKey(to=get_user_model(),on_delete=models.CASCADE,related_name='user_orders')
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(default=None,blank=True,null=True)

    class Meta :

        ordering = ('is_paid','-updated')

    def __str__(self) :
        return f'{self.user} - {str(self.id)}'

    def get_total_cost(self) :
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount :
            discount_price = (self.discount / 100) * total
            return int(total -discount_price)
        return total


class OrderItem(models.Model) :

    order = models.ForeignKey(to=Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self) :
        return str(self.id)

    def get_cost(self) :
        return self.price * self.quantity

class Coupon(models.Model) :

    coupon_code = models.CharField(max_length=30,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(90)])
    is_active = models.BooleanField(default=False)

    def __str__(self) :
        return self.coupon_code