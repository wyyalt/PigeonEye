
from django.contrib.auth import authenticate
import subprocess,random,string
from django.conf import settings
from Audit import models

from Audit.backend import ssh_interactive

class UserShell(object):
    """
    用户登录堡垒机后的shell
    """
    def __init__(self,sys_argv):
        self.sys_argv = sys_argv
        self.user = None

    def auth(self):
        count = 0
        while count < 3:
            username = input("UserName:").strip()
            password = input("PassWord:").strip()
            user = authenticate(username=username,password=password)
            #None代表认证不成功，成功返回user对象
            if not user:
                count += 1
                print("Invalid username or password!")
            else:
                self.user = user
                return True
        else:
            print("Too many attempts!")


    def start(self):
        """
        启动交互程序
        :return:
        """
        if self.auth():
            # print(self.user.account.host_user_binds.all())
            while True:
                host_groups = self.user.account.host_groups.all()
                #打印主机组
                for index,group in enumerate(host_groups):
                    print("%s.\t%s[%s]"%(index,group,group.host_user_binds.count()))

                #打印未分组的host
                print("%s.\t未分组[%s]"%(len(host_groups),self.user.account.host_user_binds.count()))

                choice = input("Select Group >>:").strip()

                if choice.isdigit():
                    choice = int(choice)
                    host_bind_list = None
                    if choice >=0 and choice < len(host_groups):
                        selected_group = host_groups[choice]
                        host_bind_list = selected_group.host_user_binds.all()
                    elif choice == len(host_groups): #选择的为未分组的机器
                        host_bind_list = self.user.account.host_user_binds.all()

                    if host_bind_list:
                        while True:
                            #打印host
                            for index, host in enumerate(host_bind_list):
                                print("%s.\t%s" % (index, host))
                            host_num = input("Select Host >>:").strip()
                            if host_num.isdigit():
                                host_num = int(host_num)
                                if host_num >= 0 and host_num < len(host_bind_list):
                                    selected_host = host_bind_list[host_num]

                                    ssh_interactive.ssh_session(selected_host,self.user)
                                    # s = string.ascii_lowercase + string.digits
                                    # random_tag = ''.join(random.sample(s,10))
                                    # session_obj = models.SessionLog.objects.create(account=self.user.account,host_user_bind=selected_host)
                                    # print("Selected Host:%s"% selected_host)
                                    # cmd = "sshpass -p %s /usr/local/openssh/bin/ssh %s@%s -p %s -o StrictHostKeyChecking=no -Z %s "%(
                                    #     selected_host.host_user.password,
                                    #     selected_host.host_user.username,
                                    #     selected_host.host.ip_addr,
                                    #     selected_host.host.port,random_tag
                                    # )
                                    # print(cmd)
                                    #
                                    # # 拼接session_tracker
                                    # session_tracker_script = "/bin/sh %s %s %s"%(
                                    #     settings.SESSION_TRACKER_SCRIPT,
                                    #     random_tag,
                                    #     session_obj.id
                                    # )
                                    # print(session_tracker_script)
                                    # # 启动session_tracker
                                    # session_tracker_obj = subprocess.Popen(session_tracker_script,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                                    # ssh_channel = subprocess.run(cmd,shell=True)
                                    # print(session_tracker_obj.stdout.read())
                            elif host_num == "back":
                                break
                elif choice == "exit":
                    break