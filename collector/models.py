from django.db import models


class billInfo(models.Model):
    billNum = models.CharField(max_length=10, default=None, unique=True)
    billName = models.CharField(max_length=300, default=None)
    billUrl = models.URLField(max_length=100, default=None, null=True, blank=True)

class billAcceptInfo(models.Model):
    bill = models.ForeignKey(billInfo)