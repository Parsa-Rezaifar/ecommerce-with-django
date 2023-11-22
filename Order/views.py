from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from . cart import Cart
from Home.models import Product
from . forms import Add_To_CardForm,CouponForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Order,OrderItem,Coupon
import requests
import json
from django.http import HttpResponse
from datetime import *
from django.contrib import messages

# Create your views here.
class CartView(View) :

    template_name = 'Order/Cart.html'

    def get(self,request):
        cart = Cart(request)
        return render(request,self.template_name,context={'cart':cart})

class Add_To_CartView(View) :

    form_class = Add_To_CardForm

    def post(self,request,product_id) :
        cart_instance = Cart(request)
        product = get_object_or_404(Product,pk=product_id)
        form = self.form_class(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            cart_instance.add_to_card(product=product,quantity=cd['quantity'])
            messages.success(request,'Product added to cart successfully',extra_tags='success')
            return redirect('Order:order')

class Remove_From_CartView(View) :

    def get(self,request,product_id) :
        cart_instance = Cart(request)
        product = get_object_or_404(Product,pk=product_id)
        cart_instance.remove_from_cart(product=product)
        messages.success(request,'Product removed from cart successfully',extra_tags='success')
        return redirect('Order:order')

class Create_OrderView(LoginRequiredMixin,View) :

    def get(self,request) :
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart :
            OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
        cart.clear_the_cart()
        return redirect('Order:order_details',order.id)

class Order_DetailView(LoginRequiredMixin,View) :

    template_name = 'Order/order.html'
    form_class = CouponForm
    def get(self,request,order_id) :
        order = get_object_or_404(Order,pk=order_id)
        form =self.form_class()
        return render(request,self.template_name,context={'order':order,'form':form})

MERCHANT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'
class Pay_OrderView(LoginRequiredMixin,View) :

    def get(self,request,order_id) :
        order = Order.objects.get(pk=order_id)
        request.session['pay_order'] = {
            'user_order' : order.id,
        }
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_cost(),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile":request.user.phone_number,"email":request.user.email}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

class Order_VerifyView(LoginRequiredMixin,View) :

    def get(self,request) :
        order_id = request.session['pay_order']['user_order']
        order = Order.objects.get(pk=int(order_id))
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK' :
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_paid = True
                    order.save()
                    return HttpResponse('Transaction success.\nRefID: ' + str(
                        req.json()['data']['ref_id']
                    ))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else :
            return HttpResponse('Transaction failed or canceled by user')

class CouponView(LoginRequiredMixin,View) :

    form_class = CouponForm

    def post(self,request,order_id):
        now = datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            discount_code = cd['coupon_code']
            try :
                coupon = Coupon.objects.get(coupon_code__exact=discount_code,valid_from__lte=now,valid_to__gte=now,is_active=True)
            except Coupon.DoesNotExist :
                messages.error(request,'This code does not exist',extra_tags='danger')
                return redirect('Order:order_details',order_id)
            order = Order.objects.get(pk=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('Order:order_details',order_id)

