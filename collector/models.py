from django.db import models


class billInfo(models.Model):
    billNum = models.CharField(max_length=10, default=None, unique=True)
    billName = models.CharField(max_length=300, default=None)
    billUrl = models.URLField(max_length=100, default=None, null=True, blank=True)

class billAcceptInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    process = models.CharField(max_length=100, default=None)
    proposeDate = models.DateField(auto_now_add=True)
    proposer = models.CharField(max_length=100, default=None)

class workers(models.Model):
    name = models.CharField(max_length=100, default=None)
    party = models.CharField(max_length=100, default="무소속")
    # 새누리당 김성태 두명 / 새누리당, 국민의당 최경환 /  