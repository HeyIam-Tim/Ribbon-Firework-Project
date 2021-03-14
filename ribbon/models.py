from django.db import models


class Ribbon(models.Model):
    ribbon_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.ribbon_name