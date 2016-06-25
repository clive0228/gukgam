from django.db import models


class billInfo(models.Model):
    billNum = models.CharField(max_length=10, default=None, unique=True)
    billName = models.CharField(max_length=300, default=None)
    billUrl = models.URLField(max_length=100, default=None, null=True, blank=True)

class billAcceptInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    process = models.CharField(max_length=100, default=None)
    proposeDate = models.DateField(default='1900-01-01')
    proposer = models.CharField(max_length=100, default=None)

class JurisJudgeInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    committee = models.CharField(max_length=100, default=None)
    sendingDate = models.DateField(default='1900-01-01')
    introDate = models.DateField(default='1900-01-01')
    disposeDate = models.DateField(default='1900-01-01')
    disposeResult = models.CharField(max_length=100, default=None)

class JurisConfInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    confName = models.CharField(max_length=300, default=None)
    confDate = models.DateField(default='1900-01-01')
    confResult = models.CharField(max_length=300, default=None)

class RelJudgeInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    relName = models.CharField(max_length=100, default=None)
    sendingDate = models.DateField(default="1900-01-01")
    introDate = models.DateField(default="1900-01-01")
    proposeDate = models.DateField(default="1900-01-01")

class LegisJudgeInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    sendingDate = models.DateField(default='1900-01-01')
    introDate = models.DateField(default='1900-01-01')
    disposeDate = models.DateField(default='1900-01-01')
    disposeResult = models.CharField(max_length=100, default=None)

class LegisConfInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    confName = models.CharField(max_length=300, default=None)
    confDate = models.DateField(default="1900-01-01")
    confResult = models.CharField(max_length=300, default=None)

class MainConfInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    introDate = models.DateField(default="1900-01-01")
    decisionDate = models.DateField(default="1900-01-01")
    confName = models.CharField(max_length=300, default=None)
    confResult = models.CharField(max_length=300, default=None)

class TransferInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    transferDate = models.DateField(default="1900-01-01")

class ProclaimInfo(models.Model):
    bill = models.ForeignKey(billInfo)
    proclaimDate = models.DateField(default="1900-01-01")
    proclaimNum = models.CharField(max_length=20, default=None)
    proclaimLaw = models.CharField(max_length=300, default=None)

class workers(models.Model):
    name = models.CharField(max_length=100, default=None)
    party = models.CharField(max_length=100, default="무소속")
    # 새누리당 김성태 두명 / 새누리당, 국민의당 최경환 /  