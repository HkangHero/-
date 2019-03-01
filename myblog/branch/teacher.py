from django.shortcuts import render,HttpResponse
from branch import models
from branch.models import Students,Teacher,Master,VoluntaryLabor
from branch.views import Password_module

import requests
from bs4 import BeautifulSoup
def login(request):
  if  request.method=='POST':
     username=request.POST.get('username')
     password=request.POST.get('password')
     s=requests.session()
     url= 'http://jwgl.just.edu.cn:8080/jsxsd/xk/LoginToXk'
     response=s.get(url)
     headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Referer': 'http://jwgl.just.edu.cn:8080/jsxsd/','Host': 'jwgl.just.edu.cn:8080','Upgrade-Insecure-Requests': '1'}
     data = {'USERNAME': username,
         'PASSWORD': password}
     response=s.post(url,data=data,headers=headers)
     soup=BeautifulSoup(response.text,"lxml")
     name=soup.select('div.block1text')
     if name:
        j=soup.select(' div.Nsb_menu_pw  div.Nsb_pw  ul li a')
        if j[2].text!='教学服务':
         token='error'
        else:
          name=name[0].text.split("<br/>")[0].split("姓名：")[1].replace('学号：','').split(" ")[0].strip()
          teacher=models.Teacher.objects.filter(teacher_id=username)
          if teacher.exists():#数据库存在则返回token
             token=teacher[0].teacher_token
          else:
            re_token=Password_module(username)
            token=re_token.create_db()
            models.Teacher.objects.create(teacher_id=username,teacher_name=name,teacher_token=token)

     else:
      token='error'
     return HttpResponse(token)



#返回老师的id
def return_id(token):
    fast=Password_module('0') #登录 
    check_token=fast.checkToken(token) #返回的老师账号
    if check_token==0:#错误token
         return 'error'
    else:  
        return check_token


import json
import time
def  somework(request):
    if request.method=='POST':
        token=request.POST.get('token')
        content=request.POST.get('content')
        contents=eval(content)
        teacher=return_id(token)
        if teacher == 'error':
             return HttpResponse('error')
        day=str(time.strftime("%Y-%m-%d", time.localtime()))
        teacher_name=models.Teacher.objects.filter(teacher_id=teacher)
        teacher_work=teacher_name[0].teacher_work
        a=[]
        worre={}
        for i in contents:  
            student=i['student_id']
            Time=i['time']
            students=models.Students.objects.filter(student_id=student)
            if students.exists():#如果学号存在就写入
               models.VoluntaryLabor.objects.create(work_id=student,time=Time,addres=teacher_work,teacher_id=teacher,date=day)
            else:#不存在说明该学生没有登录过
                worre={student}
        a.append(worre)
        return HttpResponse(json.dumps(a))

#登录以后先检查是否有工作
def check_work(request):
    if request.method=='POST':
        token=request.POST.get('token')
        fast=Password_module('0') 
        check_token=fast.checkToken(token) 
        teacher=models.Teacher.objects.filter(teacher_id=check_token)
        return HttpResponse(teacher)

#如果没有记录工作将写入
def write_work(request):
    if  request.method=='POST':
        token=request.POST.get('token')
        work=request.POST.get('work')
        fast=Password_module('0') 
        check_token=fast.checkToken(token)
        if check_token!= 'error':
            models.Teacher.objects.filter(teacher_id=check_token).update(teacher_work=work)
            return HttpResponse('ok')
        else:
            return HttpResponse('no')