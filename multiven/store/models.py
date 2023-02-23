from distutils.command.upload import upload
from unicodedata import category
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    #to have the correct plural spelling in the database
    class Meta:
        verbose_name_plural = 'Categories'
    
    #for easy naming of the categories
    def __str__(self):
        return self.title

class Product(models.Model):
    user = models.ForeignKey(User, related_name ='products', on_delete =models.CASCADE)
    category = models.ForeignKey(Category, related_name ='products', on_delete =models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # in order for the most recent added product to be at the top 
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_display_price(self):
        return self.price / 10