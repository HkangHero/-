from django.conf.urls import url
from branch import views
from branch import teacher
urlpatterns=[
 url(r'^login/',views.login),#登录
 url(r'^fastlogin/',views.fastlogin),#快速登录query
 url(r'^countwork/',views.chenck_work),#个人义工查询
 url(r'^photo/',views.post_phono),#保存个人照片
 url(r'^tlogin/',teacher.login),#老师登录
 url(r'^selwork/',teacher.write_work),#老师工作登记
 url(r'^work/',teacher.somework),#义工记录
 url(r'teacher_type/',teacher.check_work),#老师工作性质是否保存

]