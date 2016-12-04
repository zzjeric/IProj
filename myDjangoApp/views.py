# coding:utf-8
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .forms import SignInForm, SignUpForm
from .models import OrderApplication, OrderInfo,WeekReport
from .CommonUtil import *
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import auth
import tablib
import time



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


def log_out(request):
    auth.logout(request)
    return HttpResponseRedirect('/SignIn')

@login_required()
def te_dev(request):
    index = request.GET['index']
    indexDict = {'index': index, 'des': 'te_dev'}
    return render(request, 'TE_DevelopingPage.html', {
        'indexDict': json.dumps(indexDict)})


@login_required()
def meal_order_stat(request):
    indexDict = {'index': '3', 'des': 'meal_order_stat'}
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''

    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = OrderApplication.objects.count()
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    # 判断点击了【下一页】还是【上一页】还是【首页】还是【尾页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    elif pageType == 'pageFirst':
        curPage = 1
    elif pageType == 'pageLast':
        curPage = allPage
    elif pageType == 'pageSkip':
        curPage = curPage

    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    # operatedate 前面减号表示倒序
    orderApps = OrderApplication.objects.all().order_by('-operatedate')[startPos:endPos]

    return render(
        request, 'MealOrderStat.html', {
            'indexDict': json.dumps(indexDict),
            'orderApps': orderApps,
            'allPage': allPage,
            'curPage': curPage})


@login_required()
def week_report(request):
    indexDict = {'index': '2', 'des': 'week_report'}
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''

    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = WeekReport.objects.count()
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    # 判断点击了【下一页】还是【上一页】还是【首页】还是【尾页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    elif pageType == 'pageFirst':
        curPage = 1
    elif pageType == 'pageLast':
        curPage = allPage
    elif pageType == 'pageSkip':
        curPage = curPage

    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    # operatedate 前面减号表示倒序
    weekReports = WeekReport.objects.all().order_by('userName','-operatedate')[startPos:endPos]

    return render(
        request, 'WeekReport.html', {
            'indexDict': json.dumps(indexDict),
            'weekReports': weekReports,
            'allPage': allPage,
            'curPage': curPage})



@login_required()
def dialog_order(request):
    return render(request, 'Order.html')


@login_required()
def dialog_add_order(request):
    return render(request, 'AddOrder.html')


@login_required()
def dialog_add_weekreport(request):
    return render(request, 'AddWeekReport.html')


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


def ajax_add_week_report(request):
    if not validateLogin(request):
        result = {'Flag': 'N', 'Msg': 'Not Login'}
        return JsonResponse(result)
    if request.is_ajax():
        dtRange = request.POST['dtRange']
        prjName = request.POST['prjName']
        taskName = request.POST['taskName']
        planEndDt = request.POST['planEndDt']
        status = request.POST['status']
        weekReport = WeekReport(dtRange=dtRange, prjName=prjName, taskName=taskName, planEndDt=planEndDt,userName=request.user.username,
                                    operateusername=request.user.username, operatedate=datetime.now(), status=int(status))
        result = AddWeekReport(weekReport)
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

def weekreport_xlsx_download(request):
    option = request.GET.get('option', 'all')
    dtRange = request.GET.get('dtRange', None)
    if (option == 'pre' or option == 'cur') and dtRange is not None:
        weekReports = WeekReport.objects.filter(dtRange=dtRange).order_by('userName', '-operatedate')
    else:
        weekReports = WeekReport.objects.all().order_by('userName', '-operatedate')
    headers = ('序号', '姓名','时间','项目','任务','计划完成时间','完成状态')
    data = []
    if weekReports is not None and len(weekReports) > 0:
        index = 1
        for wr in weekReports:
            wr_attrs = []
            wr_attrs.append(index)
            wr_attrs.append(wr.userName)
            wr_attrs.append(wr.dtRange)
            wr_attrs.append(wr.prjName)
            wr_attrs.append(wr.taskName)
            wr_attrs.append(wr.planEndDt.strftime('%Y/%m/%d'))
            wr_attrs.append('已完成' if wr.status == 1 else '未完成')
            data.append(tuple(wr_attrs))
            index = (index + 1)
    data = tablib.Dataset(*data, headers=headers)
    the_file_name = "ExportExcels/" + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) + ".xlsx"
    with open(the_file_name, "wb") as f:
        f.write(data.xlsx)
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response
