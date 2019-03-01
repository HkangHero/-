from django.db import models

#学生信息
class Students(models.Model):
    student_id=models.CharField(max_length=12,primary_key=True) #账号
    name=models.CharField(max_length=16) #姓名
    photo=models.CharField(default=None,max_length=200,null=True) #照片
    college=models.CharField(max_length=30,null=True) #学院
    major=models.CharField(max_length=20,null=True) #专业
    phone_number=models.CharField(max_length=11,null=True)#手机号码 
    idCard=models.CharField(max_length=19,null=True)#身份证号码
    power=models.CharField(max_length=2,default=0)#该学生是否有权利查看义工审核情况
    student_token=models.CharField(max_length=300,default=None)#缓冲token
    password=models.CharField(max_length=20)#用户密码
    Pass=models.CharField(max_length=10,default='未审核')#义工是否审核
class Teacher(models.Model):
    teacher_id=models.CharField(max_length=12,primary_key=True) #老师id
    teacher_name=models.CharField(max_length=16) #姓名
    teacher_work=models.CharField(max_length=10,null=True)#负责实验室/图书馆
    teacher_token=models.CharField(max_length=300)#缓冲token
class VoluntaryLabor(models.Model):
    ud=models.AutoField(primary_key=True)
    work_id=models.CharField(max_length=12)#学生号
    teacher_id=models.CharField(max_length=12)#老师号
    date=models.CharField(max_length=10) #日期
    time=models.IntegerField()#义工时间
    addres=models.CharField(max_length=30) #实验室/还是图书馆

class Master(models.Model):
    username=models.CharField(max_length=12,primary_key=True)#账号
    password=models.CharField(max_length=20)#密码
    