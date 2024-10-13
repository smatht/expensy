from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=120)
    alt_name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'categories'
