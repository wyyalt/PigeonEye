
from Audit import models
import json
from django.db.transaction import atomic
import subprocess
from django.conf import settings
import os

class Task(object):

    def __init__(self,request):
        self.request = request
        self.task_info = json.loads(request.POST.get('task_info'))
        self.err_msg  = {}


    def is_valid(self):

        """
        验证数据
        :return:
        """
        if self.task_info:
            if self.task_info.get('task_type') == "cmd":
                if self.task_info.get('host_binds') and self.task_info.get('task_body'):
                    return True
                self.err_msg['err_info'] = "Hosts is empty or task_body is none!"
            if self.task_info.get('task_type') == "file_handler":


                print(self.task_info)
                return True

            self.err_msg['err_info'] = "Task_type identification faild!"
        self.err_msg['err_info'] = "No Data!"
        return False


    def run(self):
        """
        反射调用函数
        :return:
        """
        task_func = getattr(self,self.task_info['task_type'])
        task_id = task_func()
        return task_id

    @atomic
    def cmd(self):
        """
        :return: 任务id
        """
        print("run cmd ....")
        #写入任务信息到数据库
        task_obj = models.Task.objects.create(
            type=0,
            body=self.task_info['task_body'],
            account = self.request.user.account
        )

        host_bind_list = set(self.task_info['host_binds'])
        task_log_objs = []
        for host in host_bind_list:
            task_log_objs.append(models.TaskLog(
                task_id = task_obj.id,
                host_user_bind_id = host,
                status = 0,
            ))

        models.TaskLog.objects.bulk_create(task_log_objs,100)



        import subprocess
        cmd_str = "python3 %s %s %s"%(settings.MULTI_CMD_SCRIPT,self.task_info['task_type'],task_obj.id)
        subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)


        return task_obj.id

    @atomic
    def file_handler(self):
        """
        :return: 任务id
        """
        print("run file_handler ....")
        #写入任务信息到数据库
        task_obj = models.Task.objects.create(
            type=1,
            body=json.dumps(self.task_info['task_body']),
            account = self.request.user.account
        )

        host_bind_list = set(self.task_info['host_binds'])
        task_log_objs = []
        for host in host_bind_list:
            task_log_objs.append(models.TaskLog(
                task_id = task_obj.id,
                host_user_bind_id = host,
                status = 0,
            ))

        models.TaskLog.objects.bulk_create(task_log_objs,100)



        if self.task_info['task_body']['option_type'] == "get":
            download_path = os.path.join(settings.FILE_DOWNLOAD_BASE_PATH,str(self.request.user.id),str(task_obj.id))
            if not os.path.isdir(download_path):
                os.makedirs(download_path)


        import subprocess
        cmd_str = "python3 %s %s %s"%(settings.MULTI_CMD_SCRIPT,self.task_info['task_type'],task_obj.id)
        subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        return task_obj.id


if __name__ == "__main__":
    cmd_str = "python3 /usr/local/PigeonEye/concurrent_task.py cmd 48"
    import subprocess
    result = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result_data = result.stdout.read() + result.stderr.read()
    print(result_data.decode("utf8"))