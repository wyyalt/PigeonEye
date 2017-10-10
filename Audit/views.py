from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import json
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