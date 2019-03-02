from django.shortcuts import render,HttpResponse
from branch import models
from branch.models import Students,Teacher,Master,VoluntaryLabor,bill
from branch.views import Password_module
import requests
from bs4 import BeautifulSoup


#义工通知查询 报名
#创建义工发布单
def teacher_work(request):
    if request.method=='POST':
       title=request.POST.get('title')#内容标题
       demand=request.POST.get('demand')#男/女/无要求
       Time=request.POST.get('time')
       work_tepy=request.POST.get('work_tepy')
       work_time=request.POST.get('work_time')
       Impatient=request.POST.get('Impatient')
       photos=request.POST.get('photos')
       address=request.POST.get('address')
       phone_number=request.POST.get('phone_number')
       peoples=request.POST.get('peoples')
       models.bill.objects.create(title=title,demand=demand,time=Time,
       	work_tepy=work_tepy,work_time=work_time,Impatient=Impatient,photos=photos
       	,address=address,phone_number=phone_number,peoples=peoples)
       ##以后加订阅号通知

import time     
def find_work(request):
	if request.method=='POST':
        date=str(time.strftime("%Y-%m-%d", time.localtime()))
		models.bill.objects.filter(time__gte=date,state=0) #大于等于