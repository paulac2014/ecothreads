from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Inventory
from .models import SaleItem

@receiver(post_save, sender=Product)
def create_inventory_for_new_product(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(product=instance, stock_quantity=0)

@receiver(post_save, sender=SaleItem)
@receiver(post_delete, sender=SaleItem)
def update_sale_total(sender, instance, **kwargs):
    if instance.sale:
        instance.sale.update_total_price()