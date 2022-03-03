from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Product(models.Model):
    user = models.ForeignKey(
        User,
        default=1,
        null=True,
        related_name="products",
        on_delete=models.SET_NULL,
    )
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
