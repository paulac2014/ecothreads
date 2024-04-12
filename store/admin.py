from django.contrib import admin
from .models import Product, Inventory, Customer, Sale, SaleItem

admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Customer)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = ('customer', 'date_of_transaction', 'total_sale_price')

# Correctly registering the models
admin.site.register(Sale, SaleAdmin) # Assuming you want to manage Customers in the admin as well
# Register other models as needed
