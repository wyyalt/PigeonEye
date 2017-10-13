import sys,os


def cmd(i):
    print("cmd",i)
    return i


def file():
    pass

def callback(arg):
    print(arg)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PigeonEye.settings")
    import django
    django.setup()


    print("start.....")

    task_type = sys.argv[1]
    task_id = sys.argv[2]

    print(task_id,task_type)

    from Audit import models
    task_obj = models.Task.objects.filter(id=int(task_id)).first()
    print(task_obj)

    print(task_obj.tasklog_set.all())

    func = getattr(sys.modules[__name__],task_type)


    import multiprocessing
    pool = multiprocessing.Pool(10)
    for i in task_obj.tasklog_set.all():
        pool.apply_async(func=func,args=(123,),callback=callback)



    pool.close()
    pool.join()

