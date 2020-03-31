from django.db import models

# Create your models here.



class User(models.Model):
    """
    用户表
    """
    id = models.BigAutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=False, unique=True,verbose_name='手机号',db_index=True)
    userpic = models.CharField(max_length=128,verbose_name="用户头像url路径")
    username = models.CharField(max_length=64,null=True,verbose_name="用户名")
    password = models.CharField(max_length=128,null=True,verbose_name="密码")
    create_time = models.DateTimeField(verbose_name="创建日期",null=False,auto_now_add=True)
    status = models.CharField(max_length=4,verbose_name="用户状态")
    info = models.OneToOneField(to='UserInfo',on_delete=models.CASCADE,to_field='id')

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

class UserInfo(models.Model):
    """
    用户信息表
    """
    id = models.BigAutoField(primary_key=True)
    age = models.CharField(max_length=4)
    sex = models.CharField(max_length=4)
    qq = models.CharField(max_length=32)
    job = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    birthday = models.DateTimeField(verbose_name="出生日期",null=True)
    create_time = models.DateTimeField(verbose_name="创建日期",null=False,auto_now_add=True)


    def __str__(self):
        return self.sex

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name