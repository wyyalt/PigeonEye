import sys, os
import paramiko

import json
def cmd(task_log_obj):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=task_log_obj.host_user_bind.host.ip_addr,
            port=task_log_obj.host_user_bind.host.port,
            username=task_log_obj.host_user_bind.host_user.username,
            password=task_log_obj.host_user_bind.host_user.password
        )

        stdin, stdout, stderr = ssh.exec_command(task_log_obj.task.body) #ifconfig
        result = stdout.read() + stderr.read()
        ssh.close()

        task_log_obj.result = result
        task_log_obj.status = 1
        task_log_obj.save()
    except Exception as e:
        task_log_obj.result = e
        task_log_obj.status = 2
        task_log_obj.save()


def file_handler(task_log_obj):
    try:
        t = paramiko.Transport((task_log_obj.host_user_bind.host.ip_addr,task_log_obj.host_user_bind.host.port))

        t.connect(username=task_log_obj.host_user_bind.host_user.username,password=task_log_obj.host_user_bind.host_user.password)
        sftp = paramiko.SFTPClient.from_transport(t)

        task_body = json.loads(task_log_obj.task.body)

        from django.conf import settings

        if task_body['option_type'] == "put":

            for file in task_body['file_list']:
                file_abs_path = os.path.join(settings.FILE_UPLOAD_BASE_PATH,str(task_log_obj.task.account.user_id),file)
                remote_abs_path = os.path.join(task_body['remote_path'],file)
                sftp.put(file_abs_path,remote_abs_path)
            else:
                task_log_obj.result = 'Put Done...'
                task_log_obj.status = 1
                task_log_obj.save()

        else:
            file_list = task_body['remote_path'].split(";")
            for file in file_list:
                local_path = os.path.join(
                    settings.FILE_DOWNLOAD_BASE_PATH,
                    str(task_log_obj.task.account.user_id),
                    str(task_log_obj.task_id),
                    "%s-%s"%(str(task_log_obj.host_user_bind.host.ip_addr),os.path.basename(file)),
                )
                sftp.get(file,local_path)
            else:
                task_log_obj.result = 'Start download, and please check...'
                task_log_obj.status = 1
                task_log_obj.save()

        t.close()


    except Exception as e:
        print(e)
        task_log_obj.result = e
        task_log_obj.status = 2
        task_log_obj.save()


def callback(arg):
    print(arg)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PigeonEye.settings")
    import django

    django.setup()

    task_type = sys.argv[1]
    task_id = int(sys.argv[2])

    from Audit import models

    task_obj = models.Task.objects.filter(id=task_id).first()
    func = getattr(sys.modules[__name__], task_type)

    import multiprocessing

    pool = multiprocessing.Pool(10)
    for task_log_obj in task_obj.tasklog_set.all():
        pool.apply_async(func=func, args=(task_log_obj,))
        # pool.apply_async(func=func, args=(task_log_obj,),callback=callback)

    pool.close()
    pool.join()
