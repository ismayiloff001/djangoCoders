from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth import get_user_model

User = get_user_model()

class Category(MPTTModel, models.Model):
    # name = models.CharField(max_length=50, unique=True) # unique=True  - unik olsunlar deye istifade olunur
    name = models.CharField(max_length=50, verbose_name="Kateqoriya")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name






class Product(models.Model):

    persentage = (
        (5, '5'),
        (10, '10'),
        (15, '15'),
        (20, '20'),
        (25, '25'),
        (30, '30'),
        (35, '35'),
        (40, '40'),
        (45, '45'),
        (50, '50'),
        (55, '55'),
        (60, '60'),
        (65, '65'),
        (70, '70'),
        (75, '75'),
        (80, '80'),
        (85, '85'),
        (90, '90'),
        (95, '95'),
        (100, '100')
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kateqoriya")
    name = models.CharField(max_length=300, verbose_name="Məsulun adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıqlama")

    price = models.FloatField( verbose_name="Qiymət")
    in_sale = models.BooleanField(default=False , verbose_name="Endirimdə")
    discount_persentage = models.IntegerField(choices=persentage, null=True, blank=True, verbose_name="Endirim %")
    discount_price = models.FloatField(blank=True, null=True, verbose_name="Endirimli qiymət")
    


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  #endirimli qiymeti ozu hesablayir
        if self.in_sale:
            self.discount_price = self.price - (self.price * (self.discount_persentage / 100))
        return super().save(*args, **kwargs)

    # class Meta: # admin terefde products tabledaki cixacaq text
    #     verbose_name = "Mehsul"             # tek halda
    #     verbose_name_plural = "Mehsullar"   # cem halda

# TODO detail icinde price ve persentageleri cixart




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimage')

    def __str__(self):
        return self.product.name
