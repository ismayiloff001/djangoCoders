from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import F, FloatField, Q
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator

def index_view(request):

    categories = Category.objects._mptt_filter(parent__isnull = True)
    products = Product.objects.annotate(
        discount = Coalesce("discount_price", 0, output_field=FloatField())
    ).annotate(
        total_price = F("price") - F("discount_price")
    ).order_by("-created_at")

    context = {
        "categories": categories,
        "products": products
    }

    return render(request, "products/index.html", context)

def product_list_view(request):
    products = Product.objects.annotate(
        discount = Coalesce("discount_price", 0, output_field=FloatField())
    ).annotate(
        total_price = F("price") - F("discount_price")
    ).all()
    paginator = Paginator(products,8)
    page = request.GET.get("page",1)
    product_list = paginator.get_page(page)


    context = {
        # "products": products,   #paginationsuz

        "products": product_list, # pagination olanda
    }

    return render(request, "products/list.html", context)
