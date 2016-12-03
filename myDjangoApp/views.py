# coding:utf-8
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .forms import SignInForm, SignUpForm
from .models import OrderApplication, OrderInfo
from .CommonUtil import *
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required()
def index(request):
    index = request.GET['index']
    if index is None:
        index = 0
    indexDict = {'index': index, 'des': 'index'}
    return render(request, 'Index.html', {'indexDict': json.dumps(indexDict)})


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            result = validateSignIn(request, username, password)
            if result["Flag"] == "Y":
                return HttpResponseRedirect(reverse('meal_order_stat'))
            else:
                return render(
                    request, 'SignIn.html', {
                        'form': form, "result": result})
    else:
        form = SignInForm()
        result = {"flag": "Y", "Msg": "Empty form"}
        return render(request, 'SignIn.html', {'form': form, "result": result})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_comfirm']
            result = validateSignUp(request,username,password,password_confirm)
            if result["Flag"] == "Y":
                request.session['isLogin'] = True
                request.session['username'] = username
                return HttpResponseRedirect(reverse('meal_order_stat'))
            else:
                return render(
                    request, 'SignUp.html', {
                        'form': form, "result": result})
    else:
        form = SignUpForm()
        result = {"flag": "Y", "Msg": "Empty form"}
        return render(request, 'SignUp.html', {'form': form, "result": result})


@login_required()
def te_dev(request):
    index = request.GET['index']
    indexDict = {'index': index, 'des': 'te_dev'}
    return render(request, 'TE_DevelopingPage.html', {
        'indexDict': json.dumps(indexDict)})


@login_required()
def meal_order_stat(request):
    indexDict = {'index': '3', 'des': 'meal_order_stat'}
    # operatedate 前面减号表示倒序
    orderApps = OrderApplication.objects.all().order_by('-operatedate')
    return render(
        request, 'MealOrderStat.html', {
            'indexDict': json.dumps(indexDict),
            'orderApps': orderApps})


@login_required()
def dialog_order(request):
    return render(request, 'Order.html')


@login_required()
def dialog_add_order(request):
    return render(request, 'AddOrder.html')


def get_user_headicon(request):
    rowId = request.GET['rowId']
    result = initOrderStatList(rowId)
    return HttpResponse(result)


def ajax_add_order(request):
    if not validateLogin(request):
        result = {'Flag': 'N', 'Msg': 'Not Login'}
        return JsonResponse(result)
    if request.is_ajax():
        title = request.POST['title']
        restName = request.POST['restName']
        mealName = request.POST['mealName']
        remark = request.POST['remark']
        orderApp = OrderApplication(title=title, restname=restName, mealnames=mealName, remark=remark,
                                    operateusername=request.user.username, operatedate=datetime.now(), status=1)
        result = AddOrderApplication(orderApp)
    else:
        result = {'Flag': 'N', 'Msg': 'Not a ajax request'}
    return JsonResponse(result)


def ajax_order(request):
    if not validateLogin(request):
        result = {'Flag': 'N', 'Msg': 'Not Login'}
        return JsonResponse(result)
    if request.is_ajax():
        rowId = request.POST['rowId']
        mealName = request.POST['mealName']
        orderNum = request.POST['orderNum']
        remark = request.POST['remark']
        order = OrderInfo(orderAppId=rowId, mealname=mealName, ordernum=orderNum, remark=remark,
                          operateusername=request.user.username, operatedate=datetime.now())
        result = AddOrderInfo(order)
    else:
        result = {'Flag': 'N', 'Msg': 'Not a ajax request'}
    return JsonResponse(result)


def ajax_get_mealnames(request):
    if not validateLogin(request):
        result = {'Flag': 'N', 'Msg': 'Not Login'}
        return JsonResponse(result)
    if request.is_ajax():
        rowId = request.GET['rowId']
        result = getMealNames(rowId)
    else:
        result = {'Flag': 'N', 'Msg': 'Not a ajax request'}
    return JsonResponse(result)


def ajax_set_orderapp_finished(request):
    if not validateLogin(request):
        result = {'Flag': 'N', 'Msg': 'Not Login'}
        return JsonResponse(result)
    if request.is_ajax():
        rowId = request.GET['rowId']
        result = updateStatus(rowId)
    else:
        result = {'Flag': 'N', 'Msg': 'Not a ajax request'}
    return JsonResponse(result)


def ajax_get_orderdetail_tables(request):
    if not validateLogin(request):
        result = "<p>请先登录!</p>"
        return HttpResponse(result)
    if request.is_ajax():
        rowId = request.GET['rowId']
        result = initOrderStatTable(rowId)
        return HttpResponse(result)
    else:
        result = " <div class=\"alert alert-danger\" role=\"alert\">Opps.. There is Nothing to display...</div>"
        return HttpResponse(result)


def ajax_get_orderstat_echartsdata(request):
    if not validateLogin(request):
        result = {'Flag': 'N', 'Msg': 'Not Login'}
        return JsonResponse(result)
    if request.is_ajax():
        rowId = request.GET['rowId']
        result = getOrderStatEchartsData(rowId)
    else:
        result = {'Flag': 'N', 'Msg': 'Not a ajax request'}
    return JsonResponse(result)


def ajax_get_orderstat_list(request):
    rowId = request.GET['rowId']
    result = initOrderStatList(rowId)
    return HttpResponse(result)

def webservice_apply_qd_configuration(request):
    result = {'Flag': 'Y', 'Msg': 'Hello'}
    return JsonResponse(result)

