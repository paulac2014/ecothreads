from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

from .models import Product
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Inventory
from django.views.generic import UpdateView, ListView

from .models import Customer
from django.views.generic.list import ListView

from .models import Sale

from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from .forms import SaleForm, SaleItemFormSet  # Correct import
from django.db import transaction


from django.shortcuts import get_object_or_404, redirect, render


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'category', 'material', 'image']  # Include the 'image' field
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'category', 'material', 'image']
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'

class HomePageView(TemplateView):
    template_name = 'home.html'

@require_POST
def product_bulk_delete(request):
    product_ids = request.POST.getlist('product_ids[]')
    Product.objects.filter(pk__in=product_ids).delete()
    return JsonResponse({'status': 'success'})


@require_POST
def sale_bulk_delete(request):
    sale_ids = request.POST.getlist('sale_ids[]')
    Sale.objects.filter(id__in=sale_ids).delete()
    return JsonResponse({'status': 'success'})

def customer_bulk_delete(request):
    if request.method == 'POST':
        customer_ids = request.POST.getlist('customer_ids[]')
        Customer.objects.filter(id__in=customer_ids).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

  
class StockUpdateView(UpdateView):
    model = Inventory
    fields = ['stock_quantity']
    template_name = 'store/inventory_update_form.html'
    success_url = reverse_lazy('inventory_list')  # Ensure this URL name is defined in your urls.py

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_name'] = self.object.product.name
        return context

class StockListView(ListView):
    model = Inventory
    template_name = 'store/inventory_list.html'
    context_object_name = 'inventory_list'


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['name', 'email', 'phone']
    template_name = 'store/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['name', 'email', 'phone']
    template_name = 'store/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerListView(ListView):
    model = Customer
    template_name = 'store/customer_list.html'
    context_object_name = 'customers'

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'store/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

class CustomerSaleHistoryView(ListView):
    model = Sale
    template_name = 'store/customer_sale_history.html'
    context_object_name = 'sales'

    def get_queryset(self):
        return Sale.objects.filter(customer_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        context['customer_name'] = customer.name
        return context

# views.py


def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                created_sale = form.save(commit=False)
                formset = SaleItemFormSet(request.POST, instance=created_sale)
                if formset.is_valid():
                    created_sale.save()
                    formset.save()
                    return redirect('sale_list')
    else:
        form = SaleForm()
        formset = SaleItemFormSet()
    return render(request, 'store/sale_add_entry.html', {'form': form, 'formset': formset})

def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'store/sale_list.html', {'sales': sales})

def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        formset = SaleItemFormSet(request.POST, instance=sale)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            sale.update_total_price()  # Recalculate the total sale price
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
        formset = SaleItemFormSet(instance=sale)
    return render(request, 'store/sale_edit.html', {'form': form, 'formset': formset, 'sale': sale})



def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    if request.method == 'POST':
        sale.delete()
        return redirect('sale_list')
    return render(request, 'store/sale_confirm_delete.html', {'sale': sale})

def sale_detail(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    return render(request, 'store/sale_detail.html', {'sale': sale})