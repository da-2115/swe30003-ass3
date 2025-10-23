from rest_framework import viewsets
from .models import Product, Inventory
from .serializers import ProductSerializer, InventorySerializer
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import ProductForm, InventoryForm
from .forms import AccountForm, LoginForm, CustomerForm, CartItemForm, PaymentForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from .serializers import (
    AccountSerializer,
    CustomerSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    InvoiceSerializer,
    PaymentSerializer,
    ReportSerializer,
)
from .models import (
    Product,
    Inventory,
    Account,
    Customer,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Invoice,
    Payment,
    Report,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.prefetch_related('products').all()
    serializer_class = InventorySerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.select_related('account').all()
    serializer_class = CustomerSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.prefetch_related('items').all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items').all()
    serializer_class = OrderSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


# --- Account / Customer views ---
def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if form.is_valid() and customer_form.is_valid():
            account = form.save()
            customer = customer_form.save(commit=False)
            customer.account = account
            customer.save()
            messages.success(request, 'Account created. You can now log in.')
            return redirect('login')
    else:
        form = AccountForm()
        customer_form = CustomerForm()
    return render(request, 'inventory/register.html', {'form': form, 'customer_form': customer_form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                account = Account.objects.get(username=username)
            except Account.DoesNotExist:
                account = None
            if account and account.password_hash and check_password(password, account.password_hash):
                # store account id in session
                request.session['account_id'] = str(account.id)
                messages.success(request, 'Logged in')
                return redirect('index')
            messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'inventory/login.html', {'form': form})


def logout_view(request):
    request.session.pop('account_id', None)
    messages.info(request, 'Logged out')
    return redirect('index')


# --- Cart & checkout views ---
def view_cart(request):
    account_id = request.session.get('account_id')
    cart = None
    if account_id:
        try:
            account = Account.objects.get(id=account_id)
            cart = account.customer.cart
        except Exception:
            cart = None
    return render(request, 'inventory/cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    # simplistic add-to-cart using session/account
    account_id = request.session.get('account_id')
    if not account_id:
        messages.error(request, 'Please log in to add items to your cart')
        return redirect('login')
    account = Account.objects.get(id=account_id)
    customer = account.customer
    cart, _ = Cart.objects.get_or_create(customer=customer)
    product = Product.objects.get(id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'Added {product.name} to cart')
    return redirect('products_list')


def remove_cart_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        messages.success(request, 'Item removed')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found')
    return redirect('view_cart')


def checkout(request):
    account_id = request.session.get('account_id')
    if not account_id:
        messages.error(request, 'Please log in to checkout')
        return redirect('login')
    account = Account.objects.get(id=account_id)
    customer = account.customer
    cart = getattr(customer, 'cart', None)
    if not cart or not cart.items.exists():
        messages.error(request, 'Cart is empty')
        return redirect('view_cart')
    # create order
    order = Order.objects.create(customer=customer)
    total = 0
    for ci in cart.items.all():
        OrderItem.objects.create(order=order, product=ci.product, quantity=ci.quantity, unit_price=ci.product.price)
        total += ci.quantity * ci.product.price
    order.total = total
    order.save()
    # clear cart
    cart.items.all().delete()
    invoice = Invoice.objects.create(order=order)
    messages.success(request, 'Order placed')
    return redirect('invoice_detail', pk=invoice.id)


# --- Invoice / payment views ---
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'inventory/invoice_detail.html', {'invoice': invoice})


def pay_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            invoice.paid = True
            invoice.save()
            messages.success(request, 'Payment recorded')
            return redirect('invoice_detail', pk=invoice.id)
    else:
        form = PaymentForm()
    return render(request, 'inventory/pay_invoice.html', {'invoice': invoice, 'form': form})


# --- Reports ---
def reports_list(request):
    reports = Report.objects.all()
    return render(request, 'inventory/reports_list.html', {'reports': reports})


def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'inventory/report_detail.html', {'report': report})


# --- Simple server-rendered frontend views ---
def index(request):
    return render(request, 'inventory/index.html')


def products_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/products_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})


def inventories_list(request):
    inventories = Inventory.objects.prefetch_related('products').all()
    return render(request, 'inventory/inventories_list.html', {'inventories': inventories})


class ProductCreate(generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('products_list')


class ProductUpdate(generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('products_list')


class ProductDelete(generic.DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('products_list')


class InventoryCreate(generic.CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventories_list')


class InventoryUpdate(generic.UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventories_list')


class InventoryDelete(generic.DeleteView):
    model = Inventory
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventories_list')
