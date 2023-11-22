from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model) :

    category_name=models.CharField(max_length=100)
    category_slug=models.CharField(max_length=100,unique=True)
    subcategory = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_category',null=True,blank=True)
    is_subcategory = models.BooleanField(default=False)

    class Meta :

        ordering=('category_name',)
        verbose_name='Category'
        verbose_name_plural='Categories'

    def __str__(self):
        return self.category_name

    def get_absolute_url(self) :
        return reverse('Home:category_filter',args=[self.category_slug])

class Product(models.Model) :
    related_category=models.ManyToManyField(to=Category,related_name='products')
    product_name=models.CharField(max_length=100)
    product_slug=models.SlugField(max_length=100,unique=True)
    product_image=models.ImageField()
    product_descriptions= RichTextField()
    product_price=models.IntegerField()
    product_availability=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        ordering=('product_name',)
        verbose_name='Product'
        verbose_name_plural='Products'

    def __str__(self) :
        return self.product_name

    def get_absolute_url(self) :
        return reverse('Home:product_details',args=[self.id,self.product_slug])