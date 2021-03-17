from django.db import models

class Product(models.Model):
    name = models.CharField( max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField(blank=False)

    def __str__(self):
        return self.title




