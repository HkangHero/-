from branch import models
from branch.models import bill,Cash

#定时任务
#
#
#
#当现在时间大于记录中的时间 将会删除bill Cash 过期的日期删除
import time
def  del_db():
      get_date=str(time.strftime("%Y-%m-%d", time.localtime()))
      models.bill.objects.filter(time__lt=get_date).delete()
      models.Cash.objects.filter(pass_time__lt=get_date).delete()