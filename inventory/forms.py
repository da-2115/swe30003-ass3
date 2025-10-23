from django import forms
from .models import Product, Inventory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']


class InventoryForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 10})
    )

    class Meta:
        model = Inventory
        fields = ['name', 'products']


# Additional forms for account/customer/cart/payment flows
from django.contrib.auth.hashers import make_password, check_password
from .models import Account, Customer, CartItem, Payment


class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        account = super().save(commit=False)
        account.password_hash = make_password(self.cleaned_data['password'])
        if commit:
            account.save()
        return account


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'phone']


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'method']
