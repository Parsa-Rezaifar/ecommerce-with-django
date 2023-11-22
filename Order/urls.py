from django.urls import path
from . import views

app_name = 'Order'
urlpatterns = [
    path('create/',views.Create_OrderView.as_view(),name='create_order'),
    path('details/<int:order_id>/',views.Order_DetailView.as_view(),name='order_details'),
    path('cart/',views.CartView.as_view(),name='order'),
    path('cart/add_to_card/<int:product_id>/',views.Add_To_CartView.as_view(),name='add_to_cart'),
    path('cart/remove/<int:product_id>/',views.Remove_From_CartView.as_view(),name='remove_from_cart'),
    path('pay_order/<int:order_id>/',views.Pay_OrderView.as_view(),name='pay_order'),
    path('verify/',views.Order_VerifyView.as_view(),name='order_verify'),
    path('discount/<int:order_id>/',views.CouponView.as_view(),name='coupon'),
]