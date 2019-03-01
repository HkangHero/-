from django.shortcuts import render,HttpResponse
from qiniu import Auth,put_file,etag
import qiniu.config
from django.core import signing
#参数 上传参数的名称 文件路径
from branch import models
from branch.models import Students,Teacher,Master,VoluntaryLabor#
from django.conf import settings
import uuid
import hashlib
import json
import os
import re
#云端照片
class qiniu:
    def __init__(self,file_name,file_path):
        self.file_name=file_name
        self.file_path=file_path
    #删除云端中的文件
    def remove_photo(self):
        access_key='rXIrJdMCeuUya99Lm-XbCCViu67z39OGiEi5neqg'
        secret_key='jyulqIkhcZ9ksVnJfSgXu8tVEzhQN4rfmwXpAfbY'
        q=Auth(access_key,secret_key)
        bucket = BucketManager(q)
        bucket_name='photos'
        key=self.file_name
        ret,info = bucket.delete(bucket_name, key)
        if ret=={}:
          return 'success'
        else:
          return 'fail'
    #将文件保存到云端
    def acction_photo(self):
        access_key='rXIrJdMCeuUya99Lm-XbCCViu67z39OGiEi5neqg'
        secret_key='jyulqIkhcZ9ksVnJfSgXu8tVEzhQN4rfmwXpAfbY'
        q=Auth(access_key,secret_key)
        bucket_name='photos'
        key=self.file_name
        token=q.upload_token(bucket_name,key)
        localfile=self.file_path
        ret,info=put_file(token,key,localfile)
        if ret['key']==key and ret['hash']==etag(localfile):
             #如果成功返回 将把本地保存的图片删除
            if os.path.exists(self.file_path):
               os.remove(self.file_path)
               print('删除成功')
            return 'success'
        else:
            return 'fail'


#学生账号登录 
import requests
from bs4 import BeautifulSoup
class Login_module:
  def __init__(self,username,password):
        self.username=username
        self.password=password
  #会话
  def Get_login(self):
        s=requests.session()
        url= 'http://jwgl.just.edu.cn:8080/jsxsd/xk/LoginToXk'
        response=s.get(url)
        headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
           'Referer': 'http://jwgl.just.edu.cn:8080/jsxsd/','Host': 'jwgl.just.edu.cn:8080','Upgrade-Insecure-Requests': '1'}
        data = {'USERNAME': self.username ,
                'PASSWORD': self.password}
        response = s.post(url, data=data, headers=headers)
        return s
  #登陆成功
  def Get_session(self):
        s=self.Get_login()
        url="http://jwgl.just.edu.cn:8080/jsxsd/framework/xsMain.jsp"
        a = s.get(url).text
        soup = BeautifulSoup(a, "lxml")
        name = soup.select('div.block1text')
        name=name[0].text.split("<br/>")[0].split("姓名：")[1].replace('学号：','').split(" ")[0].strip()
        return name
  #成绩
  def Point(self):
        s=self.Get_login()
        url='http://jwgl.just.edu.cn:8080/jsxsd/kscj/cjcx_list'
        a=s.get(url).text
        soup=BeautifulSoup(a,"lxml")
        c=soup.select(' div.Nsb_pw   > table > tr > td')
        C=len(c)
        d=[]
        for i in range (1,C):  
            if i%13==0 and c[i-5].text!='任选' and len(c[i-6])!=0 :  #排除了任选课和体育课
              if c[i-11] ==c[i+2]: #去除了重修的课直接按本门课最后来取值
                 continue
              else:
                k=[]
                Xnum=0
                if c[i-9].text=='良':
                    Xnum=3.5
                elif c[i - 9].text == '优':
                    Xnum=4.5
                elif c[i - 9].text == '中':
                    Xnum = 2.5
                elif c[i - 9].text == '通过':
                    Xnum = 2.5
                else:
                   Xnum=(float(c[i - 9].text)-50)/10
                k.append(round(float(c[i - 8].text) * Xnum,4))
                k.append(float(c[i-8].text))
                k.append(c[i-12].text)
                k.append(c[i-10].text)
                d.append(k)
            else:
                pass
        if c[C-5].text!='任选'and len(c[i-6])!=0 : #因为上面的循环无法对最后一行进行判断 但觉得可以去重复
         G= []
         Xnum = 0
         if c[C - 9].text == '良':
                Xnum = 3.5
         elif c[C- 9].text == '优':
                Xnum = 4.5
         elif c[C - 9].text == '中':
                Xnum = 2.5
         elif c[C- 9].text == '通过':
                Xnum = 3
         else:
                Xnum = (float(c[C - 9].text) - 50) / 10
         G.append(round(float(c[C- 8].text) * Xnum, 4))
         G.append( float(c[C - 8].text))
         G.append(c[C- 12].text)
         G.append(c[C- 10].text)
         if  c[C-11]!=c[C-11-13]:
            d.append(G)
         elif c[C-11]==c[C-11-13] :
            d[-1:]=G
         else:
            pass
        else:
            pass
        credit=0 #学分
        Fraction=0 #单门分数
        T=[]
        D=len(d)
        for i in range (1,D) :
          t=[]
          if d[i][2] ==d[i-1][2]  :#
            credit+= d[i-1][1]
            Fraction += d[i-1][0]
            if i==D-1:
              t.append(round(Fraction / credit,2))
              t.append(d[i - 1][2])
              T.append(t)
          else:
              credit += d[i-1][1]
              Fraction += d[i-1][0]
              t.append(round(Fraction/credit,2))
              t.append(d[i-1][2])
              T.append(t)
              credit=0
              Fraction=0
        return T
  #个人信息
  def information(self):
      s=self.Get_login()
      url='http://jwgl.just.edu.cn:8080/jsxsd/grxx/xsxx'
      a=s.get(url).text
      soup=BeautifulSoup(a,"lxml" )
      label=soup.select('div.Nsb_pw > div.Nsb_layout_r > table > tr > td ')
      x_name=label[9].text.split('：')[1] #学院
      z_y=label[10].text.split('：')[1]   #专业
      id_Card=label[-7].text  #身份证
      models.Students.objects.filter(student_id=self.username).update(
            idCard=id_Card,major=z_y,college=x_name)
      return 
      
  
  #个人课程表
  def Curriculum(self):
      s= self.Get_login() 
      url='http://jwgl.just.edu.cn:8080/jsxsd/xskb/xskb_list.do'
      a=s.get(url).text
      soup=BeautifulSoup(a,"lxml")
      label=soup.select('div.kbcontent') #找出标签
      count=0 #记录序号 1-35
      ALLData=[]
      for i in label:
         curriculum=i.select('font') #查看时间段内是否安排课程
         if curriculum !=[]:
             count +=1
             xq=count%7#判断星期
             if int(count/7)==0:#第几小节
                 xj='1-2'
             elif int(count/7)==1:
                 xj='3-4'
             elif int(count/7)==2:
                 xj='5-6'
             elif int(count/7)==3:
                 xj='7-8'
             else:
                 xj='9-10'
             if re.findall('-------+',i.text ): #找出单元格中存在多个教室
                  New_str= str(i).split('---------------------')  #变成数组
                  for j in range(len(New_str)): #查看有几个冲突的课程
                      all_data = re.split(r'<[^>]*>',New_str[j])  # 把标签变成字符串 然后正则表达去除便签 返回list
                      while "" in all_data:  # 去除list空的字符全
                          all_data.remove("")
                      One_class = []
                      #对周进行处理
                      ZC=all_data[3]
                      week = all_data[3].replace('(周)', '').split(',') # 对第几周的字符串处理 [1-2,3,4-5]
                      for w in week: #对周进行处理
                          if re.findall('-',w):
                              number_day=w.split('-')
                              number_str=list(range(int(number_day[0]), int(number_day[1]) + 1))
                              for s in number_str:
                                  One_class.append(s)
                          else:
                              One_class.append(int(w))
                      all_data[3]=One_class
                      if len(all_data)==4: #冲突和不冲突的教室不一样 下面的 len(all_data)==5 而这个是4  没冲突为了安全还是输出看了一下
                        all_data.append('None')
                      json_data={'课程号':all_data[0],'课程名':all_data[1],'教师':all_data[2],'周次':ZC,'时间':all_data[3],'地点':all_data[4],'星期':xq,'小节':xj}
                      ALLData.append(json_data)
                      # print(json_data)
             else:
                  common = str(i).split('<br/>') #得到的都是字符串 变成数组去处理
                  all_data = common[0].split('>')  #得出来的是['',03S30003b-1,'']
                  ZC= re.split(r'<[^>]+>', common[3])[1] #保存该课程的时间
                  #对周进行数据晒洗
                  week = re.split(r'<[^>]+>', common[3])[1].replace('(周)', '').split(',')
                  One_class = []
                  for w in week:
                      if re.findall('-', w):
                         number_day = w.split('-')
                         number_str = list(range(int(number_day[0]), int(number_day[1]) + 1))
                         for s in number_str:
                             One_class.append(s)
                      else:
                           One_class.append(int(w))
                  #考虑体育课没有教室  print 出common[4]=='</div> 这是没有教室的
                  if common[4]=='</div>':
                       common[4]='None'
                  else:
                      common[4]= re.split(r'<[^>]+>',common[4])[1] #有教室的要进行正则匹配  格式下同
                  json_data = {'课程号': all_data[1], '课程名': common[1], '教师': re.split(r'<[^>]+>', common[2])[1], '周次': ZC, '时间': One_class,
                               '地点': common[4], '星期':xq,'小节':xj}
                  ALLData.append(json_data)
                  # print(json_data)

         else:
             #m没有排课
             count=count+1
             pass
      return ALLData




#该类对密码 token 加/解密 创建数据保存在数据库中
class Password_module:
    # TIME_OUT=30*60 #30min
    HEADER={'typ':'JWP','alg':'default'}
    KEY='JUST_16_JXJ_F'
    SALT='WWW.Kind.cn'
    def __init__(self,username):
        self.username=username
    def jia_mi(self,cls):#加密
         value=signing.dumps(cls,key=self.KEY,salt=self.SALT)
         mima=signing.b64_encode(value.encode()).decode()
         return mima    
    def jie_mi(self,cls):#解密
        s=signing.b64_decode(cls.encode()).decode()
        jie_mi=signing.loads(s,key=self.KEY,salt=self.SALT)
        return jie_mi
         
    def create_db(self):#创建 
        header=self.jia_mi(self.HEADER)
        body={"number":self.username}#token信息
        body=self.jia_mi(body)      
        md5=hashlib.md5() #md5加密
        md5.update(("%s.%s" % (header,body)).encode())
        lat=md5.hexdigest()#16进制
        token="%s.%s.%s"%(header,body,lat)
        return token

    def  get_token(self,token):
        paylode=str(token).split('.')[1]
        paylode=self.jie_mi(paylode)
        return paylode
    def checkToken(self,token):
        try:
            username=self.get_token(token)
            return username["number"] 
        except:
            return 0



#上传照片
def photo(file,username):
        url='kingzr96269.cn'
        images=[]
        #是否存在根目录 不存在则创建
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        extension=os.path.splitext(file.name)[1] #获取文件后缀名
        file_name='{}{}'.format(uuid.uuid4(),extension)#从命名
        file_path='{}{}'.format(settings.MEDIA_ROOT,file_name)#文件路径
        images.append('{}{}'.format(settings.MEDIA_URL,file_name))
        #先查该用户数据库中是否存在照片 如果存在先读取将照片在qiniu中移除 然后在上传
        login_state=models.Students.objects.filter(student_id=username)
        if login_state[0].photo!=None:
           del_photo=qiniu(login_state[0].photo,file_path)
           del_photo.remove_photo()
        with open( file_path,'wb') as f:
            for c in file.chunks():
                f.write(c)
                f.close()
        state=qiniu(file_name,file_path)
        State=state.acction_photo()
        if State=='success':
            models.Students.objects.filter(student_id=username).update(photo=file_name)
            URL=url+'/'+'{}'.format(file_name)
            return URL
        else:
             return 'fail'



#账号密码登录
def login(request):
    if request.method=='POST':
       username=request.POST.get('username')
       password=request.POST.get('password')
       try:
           state=Login_module(username,password)
           s_name=state.Get_session()
           login_state=models.Students.objects.filter(student_id=username)     
           #先判断数据库中是否保存该学生学号
           if login_state.exists():
              res_token=login_state[0].student_token
              if login_state[0].password!=password:
                  models.Students.objects.filter(student_id=username).update(password=password) 
              else:
                   pass 
              return HttpResponse(res_token)
           else:
              request_token=Password_module(username)
              get_token=request_token.create_db()
              models.Students.objects.create(student_id=username,name=s_name,student_token=get_token,
                   password=password)
              state.information()
              return HttpResponse(get_token) 
       except:
       	   return HttpResponse('error') 



#返回正确的密码
def checkloginModel(token):
    fast=Password_module('0') #登录 
    check_token=fast.checkToken(token) #返回的学生账号
    if check_token==0:#错误token
         return 'error'
    else:  
        use_date=models.Students.objects.filter(student_id=check_token)#查找学号
        password=use_date[0].password
        content=[check_token,password] #返回账号密码
        return content#返回密码



#token登录
def fastlogin(request):
    try:
        token=re.sub('"','',request.POST['token'])
    except:
        return HttpResponse("error")
    else:   
        user_date=checkloginModel(token) #获取到了密码
        #验证密码是否正确
        if user_date=='error': # token错误
           return HttpResponse('error')
        else:
            try: 
               state=Login_module(user_date[0],user_date[1])
               name=state.Get_session()
               return  HttpResponse(token) 
            except:
               return HttpResponse('invalid') #数据库中密码过期



#个人课程表
def query(request):
    if request.method=='POST':
       token=request.POST.get('token')
       state=checkloginModel(token)
       if state!='error':
          state=Login_module(state[0],state[1])
          date=state.Curriculum()
          return HttpResponse(json.dumps(date))


    
#查询义工
from django.db.models import F #排序
def chenck_work(request):
    if request.method=='POST':
       token=request.POST.get('token')
       state=checkloginModel(token)
       if state!='error':
          work_date=models.VoluntaryLabor.objects.filter(work_id=state[0])
          library=0#图书馆次数
          Other=0 #实验楼次数
          content=[]
          #判断该学生是否做过义工
          #content[0]包含做过图书馆 和 实验室的次数
          #其余的是详情
          if work_date.exists():
              for i in work_date:
                if i.addres=='图书馆':
                   library+=i.time 
                else:
                   Other+=i.time
              number={'library':library,'Other':Other}
              content.append(number)
              work=models.VoluntaryLabor.objects.filter(work_id=state[0]).order_by(F('date'),F('time'))
              for i in work:
                  c={'teacher':i.teacher_id,'date':i.date,'time':i.time,'addres':i.addres}
                  content.append(c)
              return HttpResponse(json.dumps(content))

          #没有做过义工 应该是0次
          else:
            return HttpResponse('0')
 


#上传照片
def post_phono(request):
    if request.method=='POST':
       token=request.POST.get('token')
       file=request.FILES.get('file')#获取图片
       username=checkloginModel(token)
       sate=photo(file,username[0])
       return HttpResponse(sate)


#需要token 保存 只需携带学生的账号便可 
#个人课表查询
#个人绩点查询
#个人义工查询
#三自学会报名