from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2, default=00.00)

    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    def title_in_uppercase(self):
        return self.title.upper()

    def discount(self):
        if self.price > 2222.00:
            return "Discount-LJ324"

    def __str__(self) -> str:
        return self.title
