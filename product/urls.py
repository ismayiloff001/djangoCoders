from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index_view, name="index"),
    path("list/", views.product_list_view, name="list"),
    path("about/", views.about_view, name="about"),
    # path("detail/<id>/", views.product_detail_view, name="detail"),
]
