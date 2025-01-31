from django.db import models

# Create your models here.

class DayStats(models.Model):
    date = models.DateField(unique=True);
    cups_sold = models.IntegerField(verbose_name="Cups Sold")
    cup_price = models.DecimalField(verbose_name="Price Per Cup",max_digits=10,decimal_places=2)
    total_sale = models.DecimalField(verbose_name="Total Sale",max_digits=10,decimal_places=2)
    customer_count = models.IntegerField(verbose_name="Customer Count")
    discount = models.IntegerField(verbose_name="Discount Applied (in USD)")
    profit = models.DecimalField(verbose_name="Profit / Loss",max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.date}"