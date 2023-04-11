from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe

import product.models
# Register your models here.
from .models import Category, Product, ProductImage
from .models import *



admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)