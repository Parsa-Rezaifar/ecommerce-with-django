from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from . models import Product,Category
from . import tasks
from django.contrib import messages
from utils import Is_User_AdminMixin
from Order.forms import Add_To_CardForm

# Create your views here.

class Home_PageView(View) :

    template_name = 'Home/Home_Page.html'

    def get(self,request,category_slug=None):
        products = Product.objects.filter(product_availability=True)
        categories = Category.objects.filter(is_subcategory=False)
        if category_slug :
            category = Category.objects.get(category_slug=category_slug)
            products = products.filter(related_category=category)
        return render(request,self.template_name,context={'products':products,'categories':categories})

class Product_DetailsView(View) :

    template_name = 'Home/Product_Details.html'
    form_class = Add_To_CardForm

    def get(self,request,*args,**kwargs) :
        product_details = get_object_or_404(Product,pk=kwargs['product_id'],product_slug=kwargs['product_slug'])
        form = self.form_class()
        return render(request,self.template_name,context={'product_details':product_details,'form':form})

class Home_BucketView(Is_User_AdminMixin,View) :

    template_name = 'Home/Home_Bucket.html'

    def get(self,request) :
        objects = tasks.all_bucket_objects_task()
        return render(request,self.template_name,context={'objects':objects})

class Delete_Bucket_ObjectView(Is_User_AdminMixin,View) :

    def get(self,request,key) :
        tasks.delete_bucket_object.delay(key)
        messages.success(request,'Your delete request will be done soon',extra_tags='info')
        return redirect('Home:bucket')

class Download_Bucket_ObjectView(Is_User_AdminMixin,View) :

    def get(self,request,key) :
        tasks.download_bucket_object.delay(key)
        messages.success(request,'Download request will be done soon',extra_tags='info')
        return redirect('Home:bucket')