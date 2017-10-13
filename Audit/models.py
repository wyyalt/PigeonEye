from django.db import models
from django.contrib.auth.models import User

class IDC(models.Model):
    """
    IDC信息
    """
    name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.name

class Host(models.Model):
    """
    远程主机信息
    """
    hostname = models.CharField(max_length=64,unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    idc = models.ForeignKey("IDC")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "%s-%s"%(self.hostname,self.ip_addr)

class HostGroup(models.Model):
    """
    主机组
    """
    name = models.CharField(max_length=64, unique=True)
    host_user_binds = models.ManyToManyField("HostUserBind")

    def __str__(self):
        return self.name

class HostUser(models.Model):
    """
    存储远程主机用户信息
    """
    auth_type_choices = (
        (0,'ssh-password'),
        (1,'ssh-key')
    )
    auth_type = models.SmallIntegerField(choices=auth_type_choices)
    username = models.CharField(max_length=32)
    password = models.CharField(blank=True,null=True,max_length=128)

    class Meta:
        unique_together = ('username','password')

    def __str__(self):
        return "%s-%s-%s"%(self.get_auth_type_display(),self.username,self.password)

class HostUserBind(models.Model):
    """
    绑定主机和用户
    """
    host = models.ForeignKey("Host")
    host_user =  models.ForeignKey("HostUser")

    def __str__(self):
        return "%s-%s"%(self.host,self.host_user)

class Token(models.Model):
    """
    存储登录token
    """
    host_user_bind = models.ForeignKey("HostUserBind")
    token = models.CharField(max_length=128,unique=True)
    account = models.ForeignKey("Account")
    timeout = models.IntegerField(default=300)
    token_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('host_user_bind','token')

    def __str__(self):
        return "%s-%s"%(self.host_user_bind,self.token)


class SessionLog(models.Model):
    account = models.ForeignKey("Account")
    host_user_bind = models.ForeignKey("HostUserBind")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return "%s-%s"%(self.account,self.host_user_bind)


class AuditLog(models.Model):
    """
    审计日志
    """
    session_log = models.ForeignKey("SessionLog")
    command = models.TextField(max_length=1024)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return "%s-%s-%s-%s"%(self.session_log,self.command,self.start_date,self.end_date)

class Account(models.Model):
    """
    堡垒机账户信息
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64)
    host_user_binds =  models.ManyToManyField("HostUserBind",blank=True)
    host_groups = models.ManyToManyField("HostGroup",blank=True)

    def __str__(self):
        return "%s-%s"%(self.user,self.name)


class Task(models.Model):
    """
    任务信息
    """
    type_choice = ((0,'cmd'),(1,'file'))
    type = models.SmallIntegerField(choices=type_choice)
    body = models.TextField(max_length=1024)
    account = models.ForeignKey("Account")
    timeout = models.IntegerField(default=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s-%s-%s-%s"%(self.id,self.account,self.type,self.body,self.date)


class TaskLog(models.Model):
    """
    任务结果
    """
    task = models.ForeignKey("Task")
    host_user_bind = models.ForeignKey("HostUserBind")
    status_choice = (
        (0,'init'),
        (1,'success'),
        (2,'failed'),
        (3,'timeout'),
    )
    status = models.SmallIntegerField(choices=status_choice)
    result = models.TextField(blank=True,default="Waiting...")

    class Meta:
        unique_together = ('task','host_user_bind')


    def __str__(self):
        return "%s-%s-%s-%s-%s"%(self.task_id,self.task,self.host_user_bind,self.status,self.result)






