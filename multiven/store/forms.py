#Django default form

from django import forms

from .models import Product, Order, PaymentMade

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'zipcode', 'city', 'phone_number',)


# Modelform is used to generate forms based on the data base form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image',)
        widgets = {
            'category' : forms.Select(attrs={
                'class' : 'w-full p-3 border border-gray-900'
            }),
            'title' : forms.TextInput(attrs={
                'class' : 'w-full p-3 border border-gray-900'
            }),
            'description' : forms.Textarea(attrs={
                'class' : 'w-full p-3 border border-gray-900'
            }),
            'price' : forms.TextInput(attrs={
                'class' : 'w-full p-3 border border-gray-900'
            }),
            'image' : forms.FileInput(attrs={
                'class' : 'w-full p-3 border border-gray-900'
            })
        }

class Payform(forms.ModelForm):
    class Meta:
        model = PaymentMade
        fields = ('delivery_address', 'delivery_city', 'delivery_phone',)