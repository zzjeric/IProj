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