from django.db import models
from account.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table="category"



    
class Product(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/', null=True ,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    createuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    # 1 はカテゴリ ID
    def __str__(self):
        return self.name
    
    class Meta:
        db_table="product"

class chatlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    text = models.TextField()
    hostuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='hosted_chats')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='participated_chats')
    time = models.DateTimeField()