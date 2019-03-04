from django.shortcuts import render,HttpResponse
from branch import models
from branch.models import bill,Cash,Teacher
from branch.views import Password_module
import requests
from bs4 import BeautifulSoup
from branch.teacher import return_id


#义工通知查询 报名
#创建义工发布单
def teacher_work(request):
    if request.method=='POST':
       token=request.POST.get('token')#获取老师token
       title=request.POST.get('title')#内容标题
       demand=request.POST.get('demand')#男/女/无要求
       Time=request.POST.get('time')
       work_time=request.POST.get('work_time')
       Impatient=request.POST.get('Impatient')
       photos=request.POST.get('photos')
       address=request.POST.get('address')
       phone_number=request.POST.get('phone_number')
       peoples=request.POST.get('peoples')
       teacher_id=return_id(token)
       if teacher_id == 'error':
             return HttpResponse('error') 
       work_tepy=models.Teacher.objects.filter(teacher_id=teacher_id)[0].teacher_work
       models.bill.objects.create(title=title,demand=demand,time=Time,
        work_tepy=work_tepy,work_time=work_time,Impatient=Impatient,photos=photos,
        address=address,phone_number=phone_number,peoples=int(peoples),teacher_name=teacher_id)
       ##以后加订阅号通知
       return HttpResponse('ok')



#查找出今天或者今天以后的招募义工返回json
#没有便返回None
#bill与Case之间进行对比 如果该学生已经报名了 那么在界面上应该变成灰色 不可报名  正常则是可以报名
#
import time
import json
from django.db.models import F #排序     
def find_work(request):
    if request.method=='GET':
        token=request.GET.get('token')
        stu_id=return_id(token)
        if stu_id == 'error':
             return HttpResponse('error') 
        date=str(time.strftime("%Y-%m-%d", time.localtime()))#获取当时的日期
        #筛选出大于等于日期 并且人数没有报完。
        content=[]
        is_null=models.bill.objects.filter(time__gte=date).order_by(F('time')) #大于等于
        if is_null.exists():
            for i in is_null:
                stu=models.Cash.objects.filter(cid=i.ud,pass_time=stu_id) #在CASE中查找该任务的id与该学生的id 如果有则说明该学生已经报名了
                if stu.exists():
                    c=1
                else:
                    c=0
                if i.number_peoplr<i.peoples :#如果bill中的报名人数小于选择需要的人数 则显示
                    number={'title':i.title,'demand':i.demand,'time':i.time,'typt':i.work_tepy,'needtime':i.work_time,'name':i.teacher_name,
                    'Impatient':i.Impatient,'photos':i.photos,'address':i.address,
                    'phone_number':i.phone_number,'peoples':i.peoples,'number_peoplr':i.number_peoplr,'c':c}
                    content.append(number)
            return HttpResponse(json.dumps(content))
        else:
           return HttpResponse('None')


#学生报名义工 
#先判断Bill中记录 如果报名的人数=需要人数 则人数满
#如果CASH已经存在了 就是报名重复
#否则 记录
def signworks(request):
  if request.method=='POST':
     token=request.POST.get('token')#学生
     uid=request.POST.get('id')#bill账单中的ud
     students=return_id(token)
     if students == 'error': 
           return HttpResponse('学生token错误')
     se_sql=models.bill.objects.filter(ud=uid)
     number=se_sql[0].number_peoplr
     if number==se_sql[0].peoples:
         return HttpResponse('overflow') #人数已经满
     sta=models.Cash.objects.filter(ud=uid,student_id=students)
     if sta.exists():
          return HttpResponse('你已参加报名')
            #先将bill中的保名人数加一
     date=str(time.strftime("%Y-%m-%d", time.localtime()))
     models.bill.objects.filter(ud=uid).update(number_peoplr=number+1)
     models.Cash.objects.create(cid=uid,student_id=students,pass_time=date) 
     return HttpResponse('ok')



#查询自己正在接到的任务
#要判断返回的不为空
#查找Cash中 所有事件的时间大于等于当天时间
#也没有必要 因为在定时任务的时候要都会删除 
#
def process(request):
    if request.method=='POST':
       token=request.POST.get('token')
       students=return_id(token)
       content=[]
       if students == 'error': 
          return HttpResponse('学生token错误')
       else:
          date=str(time.strftime("%Y-%m-%d", time.localtime()))
          data=models.Cash.objects.filter(student_id=students,pass_time__gte=date)
          if data.exists():  
            for i in data:
              ex=models.bill.objects.filter(ud=i.cid)
              #Case中筛选出 符合条件的Ud 在bill中查找出便可 
              if ex.exists():
                    lis={'phone':ex[0].photos,'time':ex[0].time,'address':ex[0].address,'id':ex[0].ud}
                    content.append(lis)
          return HttpResponse(json.dumps(content))


#取消报名义工
#先将bill中的报名人数减一
#然后在Case中删除该学生的记录
def del_process(request):
   if request.method=='POST':
      ud=request.POST.get('id')
      token=request.POST.get('token')
      stu_id=return_id(token)
      if stu_id == 'error':
             return HttpResponse('error') 
      date=models.bill.objects.filter(ud=ud)
      if date.exists():
         num=date[0].number_peoplr-1
         models.bill.objects.filter(ud=ud).update(number_peoplr=num)
         #
         models.Case.objects.filter(cid=ud,student_id=stu_id).delete()
         return HttpResponse('ok')
      else:
        return HttpResponse('no')