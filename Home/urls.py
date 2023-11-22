from django.urls import path,include
from . import views

app_name = 'Home'

bucket_urls = [
    path('', views.Home_BucketView.as_view(), name='bucket'),
    path('delete_obj/<str:key>/', views.Delete_Bucket_ObjectView.as_view(), name='delete_bucket_obj'),
    path('download_obj/<str:key>/', views.Download_Bucket_ObjectView.as_view(), name='download_bucket_obj'),
]

urlpatterns = [
    path('',views.Home_PageView.as_view(),name='home'),
    path('category/<slug:category_slug>/',views.Home_PageView.as_view(),name='category_filter'),
    path('bucket/',include(bucket_urls)),
    path('product/details/<int:product_id>/<slug:product_slug>/',views.Product_DetailsView.as_view(),name='product_details'),
]