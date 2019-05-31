"""
数据查询系统：数据库 ORM 模块
@Author  : JK Wang
@Time    : 2019/4/20 17:02
"""
from django.db import models
import django.utils.timezone as timezone

# Create your models here.


class Log(models.Model):
    """
    检测记录表单
    """
    time = models.DateTimeField(auto_now_add=True)
    detect_class = models.CharField(max_length=10)
    path = models.CharField(max_length=60, null=True)

    def __str__(self):
        return "<Log:(id:%s,class:%s)>" % (self.id, self.time)

    class Meta:
        db_table = 'detection_log'


class State(models.Model):
    """
    缺陷图片表单
    """
    run_state = models.CharField(max_length=10)
    uph = models.IntegerField()
    detection_num = models.IntegerField()
    defect_num = models.IntegerField()

    def __str__(self):
        return "<State: %s)>" % self.run_state

    class Meta:
        db_table = 'running_state'


class Chart(models.Model):
    """
    缺陷图片表单
    """
    step_1 = models.FloatField()
    step_2 = models.FloatField()
    step_3 = models.FloatField()
    step_4 = models.FloatField()

    class Meta:
        db_table = 'chart_data'


class User(models.Model):
    """
    用户信息表单
    """
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)

    class Meta:
        db_table = 'user'
