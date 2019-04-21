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
    path = models.CharField(max_length=30, null=True)

    def __str__(self):
        return "<Log:(id:%s,class:%s)>" % (self.id, self.time)

    class Meta:
        db_table = 'detection_log'


class Defect(models.Model):
    """
    缺陷图片表单
    """
    path = models.CharField(max_length=20)

    def __str__(self):
        return "<Defect:(id:%s)>" % self.path

    class Meta:
        db_table = 'defect_log'


class User(models.Model):
    """
    用户信息表单
    """
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)

    class Meta:
        db_table = 'user'
