from django.conf.urls import url
from branch import views,teacher,works
urlpatterns=[
 url(r'^login/',views.login),#登录
 url(r'^fastlogin/',views.fastlogin),#快速登录query
 url(r'^countwork/',views.chenck_work),#个人义工查询
 url(r'^photo/',views.post_phono),#保存个人照片
 url(r'^tlogin/',teacher.login),#老师登录
 url(r'^selwork/',teacher.write_work),#老师工作登记
 url(r'^work/',teacher.somework),#义工记录
 url(r'teacher_type/',teacher.check_work),#老师工作性质是否保存
 url(r'teacher_work/',works.teacher_work),#老师发布义工信息
 url(r'find_work/',works.find_work),#学生查找发布的义工
 url(r'signworks/',works.signworks),#学生报名做义工
 url(r'process/',works.process),#学生查询自己现在接到义工任务
]