#Django default form

from django import forms

from .models import Product


# Modelform is used to generate forms based on the data base form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image',)