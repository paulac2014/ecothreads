import json
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)


    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.stock_quantity} in stock"
    
    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventory"

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # Allows for optional phone numbers


    def __str__(self):
        return f"{self.name} ({self.email})"



class Sale(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    date_of_transaction = models.DateTimeField(default=timezone.now)
    total_sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Sale #{self.id} to {self.customer} on {self.date_of_transaction.strftime('%Y-%m-%d')}"

    def update_total_price(self):
        total_price = sum(item.get_total_price() for item in self.saleitem_set.all())
        self.total_sale_price = total_price
        self.save()
        
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            self.price_at_sale = self.product.price
        
        super().save(*args, **kwargs)  # Save the SaleItem first

        if is_new:  # Ensure we only adjust inventory for new SaleItems
            # Update inventory stock
            inventory = Inventory.objects.get(product=self.product)
            inventory.stock_quantity -= self.quantity
            inventory.save()
        
        # After saving the SaleItem and adjusting inventory, update Sale's total price
        if hasattr(self, 'sale'):
            self.sale.update_total_price()

    def get_total_price(self):
        return self.quantity * self.price_at_sale