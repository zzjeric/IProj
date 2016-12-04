"""DjangoDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myDjangoApp import views as myDjangoApp_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^SignIn',myDjangoApp_views.sign_in,name='sign_in'),
    url(r'^SignUp',myDjangoApp_views.sign_up,name='sign_up'),
    url(r'^LogOut',myDjangoApp_views.log_out,name='log_out'),
    url(r'^Index',myDjangoApp_views.index,name='index'),
    url(r'^TE_Dev',myDjangoApp_views.te_dev,name='te_dev'),
    url(r'^MealOrderStat',myDjangoApp_views.meal_order_stat,name='meal_order_stat'),
    url(r'^WeekReport',myDjangoApp_views.week_report,name='week_report'),
    url(r'^Dialog/Order',myDjangoApp_views.dialog_order,name='dialog_order'),
    url(r'^Dialog/AddOrder',myDjangoApp_views.dialog_add_order,name='dialog_add_order'),
    url(r'^Dialog/AddWeekReport',myDjangoApp_views.dialog_add_weekreport,name='dialog_add_weekreport'),
    url(r'^Ajax/AddOrder',myDjangoApp_views.ajax_add_order,name='ajax_add_order'),
    url(r'^Ajax/AddWeekReport',myDjangoApp_views.ajax_add_week_report,name='ajax_add_week_report'),
    url(r'^Ajax/Order',myDjangoApp_views.ajax_order,name='ajax_order'),
    url(r'^Ajax/GetMealNames',myDjangoApp_views.ajax_get_mealnames,name='ajax_get_mealnames'),
    url(r'^Ajax/SetOrderAppFinished',myDjangoApp_views.ajax_set_orderapp_finished,name='ajax_set_orderapp_finished'),
    url(r'^Ajax/GetOrderDetailTables',myDjangoApp_views.ajax_get_orderdetail_tables,name='ajax_get_orderdetail_tables'),
    url(r'^Ajax/GetOrderStatEchartsData',myDjangoApp_views.ajax_get_orderstat_echartsdata,name='ajax_get_orderstat_echartsdata'),
    url(r'^Ajax/GetOrderStatList',myDjangoApp_views.ajax_get_orderstat_list,name='ajax_get_orderstat_list'),
    url(r'^Download/WeekReportExportExcel',myDjangoApp_views.weekreport_xlsx_download,name='weekreport_xlsx_download'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
