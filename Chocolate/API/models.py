from django.db import models
from Chocolate import settings
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    title=models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Chocolates(models.Model):
    title = models.CharField(max_length = 200)
    category = models.ForeignKey(Category,related_name='chocolates',on_delete=models.CASCADE)
    description = models.CharField(max_length = 500, default=None)
    price = models.FloatField(null=True, blank=True)
    image_url = models.URLField(max_length = 2083, default=False)
    choco_available = models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
     #image = models.ImageField(upload_to =' ',blank=True,null=True)

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title


class Order(models.Model):
    product = models.ForeignKey(Chocolates, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class CartItem(models.Model):
    customer = models.OneToOneField(User,
                                    related_name='cart', on_delete=models.CASCADE, )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        Chocolates,
        related_name='items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.product.title, self.quantity)

