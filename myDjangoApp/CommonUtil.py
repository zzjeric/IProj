#!/usr/bin/python3
#-*-coding:utf-8-*-
# Author : EricZhao 2016-10-24
from .models import OrderApplication,OrderInfo
from django.db.models import Count
from django.db.models import Sum
from django.core import serializers
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
import pytz

def validateLogin(request):
    try:
        if request.user.is_authenticated():
            return True
        else:
            return False
    except:
        return False

def validateSignIn(request,username,password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return {"Flag": "Y", "Msg": "Success"}
        else:
            {"Flag": "N", "Msg": "Error: 帐户已禁用！"}
    else:
        return {"Flag": "N", "Msg": "Error: 用户名或密码不正确"}



def validateSignUp(request,username,password,password_confirm):
    if password != password_confirm:
        result = {"Flag": "N", "Msg": "两次密码输入不一致!"}
    user = authenticate(username=username, password=password)
    if user is not None:
        return {"Flag": "N", "Msg": "Error: User already exist"}
    else:
        user = User.objects.create_user(username=username, password=password)
        login(request,user)
        return {"Flag": "Y", "Msg": "Success"}



def AddOrderApplication(orderApp):
    try:
        orderApp.save()
        return {"Flag": "Y", "Msg": "Success"}
    except Exception as e:
        return {"Flag": "N", "Msg": "Error: "+e}

def AddWeekReport(weekReport):
    try:
        weekReport.save()
        return {"Flag": "Y", "Msg": "Success"}
    except Exception as e:
        return {"Flag": "N", "Msg": "Error: "+e}


def AddOrderInfo(order):
    try:
        order.save()
        return {"Flag": "Y", "Msg": "Success"}
    except Exception as e:
        return {"Flag": "N", "Msg": "Error: "+e}


def getMealNames(rowid):
    try:
        orderApp = OrderApplication.objects.get(id=rowid)
        if orderApp.mealnames is None:
            return {"Flag": "N", "Msg": "Error: Empty Mealnames"}
        else:
            return {"Flag": "Y", "Msg": "Success","Data":orderApp.mealnames}
    except:
        return {"Flag": "N", "Msg": "Error: OrderApplication not exist"}


def updateStatus(rowid):
    try:
        orderApp = OrderApplication.objects.get(id=rowid)
        orderApp.status = 0
        orderApp.save()
        return {"Flag": "Y", "Msg": "Success"}
    except:
        return {"Flag": "N", "Msg": "Error: OrderApplication not exist"}



def initOrderStatTable(rowid):
    orderInfos = OrderInfo.objects.filter(orderAppId=rowid)
    tz = pytz.timezone('Asia/Shanghai')
    if orderInfos is not None and len(orderInfos) > 0:
        result = "<table class=\"table table-striped\">";
        result += "<thead>"
        result += "<tr>"
        result += "<th>序号</th><th>预订人</th><th>美食名称</th><th>数量</th><th>预定时间</th>"
        result += "</tr>"
        result += "</thead>"
        result += "<tbody>"
        index = 1;
        for orderInfo in orderInfos:
            result += "<tr>"
            result += "<td>" + str(index) + "</td>"
            result += "<td>" + orderInfo.operateusername + "</td>"
            result += "<td>" + orderInfo.mealname + "</td>"
            result += "<td>" + str(orderInfo.ordernum) + "</td>"
            result += "<td>" + orderInfo.operatedate.astimezone(tz).strftime('%y-%m-%d %H:%M:%S') + "</td>"
            result += "</tr>"
            index = index + 1

        result += "</tbody>"
        result += "</table>"
    else:
        result = " <div class=\"alert alert-danger\" role=\"alert\">Opps.. There is Nothing to display...</div>"
    return result

def getOrderStatEchartsData(rowid):
    result = []
    queryresult = OrderInfo.objects.filter(orderAppId=rowid).values('mealname').annotate(dcount=Sum('ordernum'))
    if queryresult is not None and len(queryresult) > 0:
        for s in queryresult:
            # print(s)
            result.append({"value":s['dcount'],"name":s['mealname']})
        # print(result)
        # result = serializers.serialize('json', result)
    return {'Flag': 'Y', 'Msg': 'Success','Data':result}


def initOrderStatList(rowid):
    result = ""
    queryresult = OrderInfo.objects.filter(orderAppId=rowid).values('mealname').annotate(dcount=Count('mealname'))
    if queryresult is not None and len(queryresult) > 0:
        for s in queryresult:
            # result += "<li>"+s['mealname']+"<span class=\"badge\">"+s['dcount']+"</span></li>"
            result += "<li><button style=\"margin:2px;\" class=\"btn btn-primary\" type=\"button\">  " + s['mealname'] + "  <span class=\"badge\">" + str(s['dcount']) + "</span></button></li>"
    return result


def file_iterator(file_name, chunk_size=512):
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break



