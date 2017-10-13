import sys, os
import paramiko


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

        stdin, stdout, stderr = ssh.exec_command(task_log_obj.task.body)
        result = stdout.read() + stderr.read()
        ssh.close()

        task_log_obj.result = result
        task_log_obj.status = 1
        task_log_obj.save()
    except Exception as e:
        task_log_obj.result = e
        task_log_obj.status = 2
        task_log_obj.save()


def file():
    pass


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
