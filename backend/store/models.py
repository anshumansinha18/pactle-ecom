from django.db import models


from django.db import models



class Product(models.Model):
    # Product Model:
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    inventory_count = models.PositiveIntegerField()
    image_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

