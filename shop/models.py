from django.db import models
from django.urls import reverse
from pyuploadcare.dj.models import ImageField
from taggit.managers import TaggableManager




class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ImageField(blank=True, null=True, manual_crop="4:4",)
    title = models.CharField(max_length=150, db_index=True)
    

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])



class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)


    class Meta:
        ordering = ('name', )
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory', args=[self.slug])


class MiniCategory(models.Model):
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'minicategory'
        verbose_name_plural = 'minicategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    minicategory = models.ForeignKey(MiniCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    reject_price = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ImageField(blank=True, null=True, manual_crop="4:4",)
    tags = TaggableManager()
    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
    @property
    def original_price(self,request):
    	
    	return self.price 
    	

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
