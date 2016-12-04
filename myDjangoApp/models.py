from django.db import models


class OrderApplication(models.Model):
    # rowid = models.IntegerField()
    operateusername = models.CharField(max_length=20)
    operatedate = models.DateTimeField()
    title = models.CharField(max_length=50)
    restname = models.CharField(max_length=50)
    mealnames = models.CharField(max_length=512)
    status = models.IntegerField(default=1)
    remark = models.CharField(max_length=512,null=True)

class OrderInfo(models.Model):
    orderAppId = models.IntegerField()
    operateusername = models.CharField(max_length=20)
    operatedate = models.DateTimeField()
    mealname = models.CharField(max_length=30)
    ordernum = models.IntegerField()
    remark = models.CharField(max_length=512,null=True)

class WeekReport(models.Model):
    operateusername = models.CharField(max_length=20)
    operatedate = models.DateTimeField()
    userName = models.CharField(max_length=30)
    prjName = models.CharField(max_length=50)
    taskName = models.CharField(max_length=128)
    planStartDt = models.DateTimeField(null=True)
    planEndDt = models.DateTimeField()
    status = models.IntegerField(default=0)
    dtRange = models.CharField(max_length=50)
    remark = models.CharField(max_length=512, null=True)