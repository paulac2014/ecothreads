from django.urls import path
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductDetailView
from .views import StockListView, StockUpdateView
from .views import CustomerCreateView, CustomerUpdateView, CustomerDeleteView, CustomerSaleHistoryView, CustomerListView
from .views import add_sale, sale_list, edit_sale, delete_sale, sale_detail
from .views import product_bulk_delete, sale_bulk_delete, customer_bulk_delete

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/bulk-delete/', product_bulk_delete, name='product_bulk_delete'),

    path('inventory/', StockListView.as_view(), name='inventory_list'),
    path('inventory/<int:pk>/update/', StockUpdateView.as_view(), name='stock_update'),

    path('customer/', CustomerListView.as_view(), name='customer_list'),
    path('customer/add/', CustomerCreateView.as_view(), name='customer_add'),
    path('customer/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('customer/<int:pk>/sales/', CustomerSaleHistoryView.as_view(), name='customer_sale_history'),
    path('customer/bulk-delete/', customer_bulk_delete, name='customer_bulk_delete'),

    path('sale/add/', add_sale, name='sale_add'),
    path('sale/<int:sale_id>/edit/', edit_sale, name='sale_edit'),
    path('sale/<int:sale_id>/delete/', delete_sale, name='sale_delete'),
    path('sale/<int:sale_id>/', sale_detail, name='sale_detail'),
    path('sale/', sale_list, name='sale_list'),
    path('sale/bulk-delete/', sale_bulk_delete, name='sale_bulk_delete')
]



