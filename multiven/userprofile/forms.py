from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models import Order



class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1' ,'password2' )
        widgets = {
            'username' : forms.TextInput({
                'class' : 'w-full p-3 border border-gray-900'
            }),
        }

class ConfirmForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'zipcode', 'city', 'phone_number',)
        widgets = {
            'username' : forms.TextInput({
                'class' : 'w-full'
            }),
        }