from django.db import models


class Categories(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=120)
    alt_name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'categories'


class Records(models.Model):
    id = models.CharField(max_length=40, primary_key=True, db_column='id')
    description = models.CharField(max_length=350, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    category = models.ForeignKey(Categories, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    sync = models.BooleanField(default=False)
    source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'records'
