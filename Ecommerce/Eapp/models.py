from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
# Create your models here.

class Product(models.Model):
    CAT=((1,"shoes"),(2,"mobile"),(3,"cloths"))
    pname = models.CharField(max_length=255,verbose_name="Product Name" ,default="")
    price = models.IntegerField()
    category=models.IntegerField(choices=CAT, verbose_name="Category" ,default=0)
    description=models.CharField(max_length=100, verbose_name="Details", default="")
    is_active=models.BooleanField(default=True, verbose_name="Is_Available")
    pimage=models.ImageField(upload_to='image')  # use to upload image
    
    def __str__(self):
        return self.pname
    
class Cart(models.Model):
    userid=models.ForeignKey('auth.user',on_delete=models.CASCADE,db_column="userid")
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE,db_column="user_id")
    p_id=models.ForeignKey("Product",on_delete=models.CASCADE,db_column="p_id")
    qty=models.IntegerField(default=1)
    amt=models.FloatField()