from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json,os
import zipfile
from Audit import models
import string,random
import datetime
from django.conf import settings
from wsgiref.util import FileWrapper
# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def host_list(request):
    return render(request,'hostlist.html')

def user_login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            return render(request, 'login.html',{'err_msg':"Username or Password was Wrong!"})

@login_required
def user_logout(request):
    logout(request)
    return redirect('/login.html')

def get_hosts(request):
    group_id = request.GET.get('gid')
    if group_id == "-1":
        host_list = request.user.account.host_user_binds.values(
            'id','host__hostname','host__ip_addr','host__port','host__idc__name','host_user__username'
        )
    else:
        group_obj = request.user.account.host_groups.get(id=group_id)
        host_list = group_obj.host_user_binds.values(
            'id','host__hostname','host__ip_addr','host__port','host__idc__name','host_user__username'
        )

    return HttpResponse(json.dumps(list(host_list)))


def token(request):
    host_user_bind_id = request.POST.get('hub_id')

    exist_timeout = datetime.datetime.now() - datetime.timedelta(seconds=300)
    token_obj = models.Token.objects.filter(host_user_bind_id=host_user_bind_id,token_date__gt=exist_timeout).first()
    if token_obj:
        return HttpResponse(json.dumps({'token':token_obj.token}))
    else:

        token_str = ''.join(random.sample(string.ascii_lowercase + string.digits,8))


        models.Token.objects.create(
            host_user_bind_id = host_user_bind_id,
            token = token_str,
            account = request.user.account
        )
        return HttpResponse(json.dumps({'token': ''.join(token_str)}))

@login_required
def multi_cmd(request):
    return render(request, 'multicmd.html')


@login_required
@csrf_exempt
def file_handler(request):
    if request.method == "POST":


        file_obj = request.FILES.get('file')
        import os
        file_abs_path = os.path.join(settings.FILE_UPLOAD_BASE_PATH,str(request.user.id),file_obj.name)
        if not os.path.isdir(os.path.dirname(file_abs_path)):
           os.makedirs(os.path.dirname(file_abs_path))

        if not os.path.exists(file_abs_path):
            with open(file_abs_path,'wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

        response = HttpResponse('success')
        response.status_code = 200
        return response

    if request.method == "GET":
        return render(request, 'filehandler.html')

from Audit.backend import task_handler


@login_required
def multi_task(request):

    task_obj = task_handler.Task(request)

    if task_obj.is_valid():
        result = task_obj.run()
        return HttpResponse(result)

@login_required
def task_result(request):
    task_id = request.GET.get('task_id')
    result_list = list(models.TaskLog.objects.filter(task__id=task_id).values(
        'task__id',
        'host_user_bind__host__ip_addr',
        'host_user_bind__host_user__username',
        'result',
        'status'
        )
    )
    print(result_list)
    return HttpResponse(json.dumps(result_list))

@login_required
def download_file(request):
    task_id = request.GET.get('task_id')

    zip_file_name = "task-%s-files"%task_id

    archive = zipfile.ZipFile(zip_file_name,'w',zipfile.ZIP_DEFLATED)
    file_path = os.path.join(settings.FILE_DOWNLOAD_BASE_PATH,str(request.user.id),str(task_id))
    file_list = os.listdir(file_path)

    for filename in file_list:
        archive.write('%s/%s'%(file_path,filename),arcname=filename)
    archive.close()

    wrapper = FileWrapper(open(zip_file_name,'rb'))
    response = HttpResponse(wrapper,content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip'%zip_file_name
    response['content-Length'] = os.path.getsize(zip_file_name)

    return response