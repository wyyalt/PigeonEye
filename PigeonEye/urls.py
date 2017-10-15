"""PigeonEye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Audit import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^hostlist.html$', views.host_list,name='hostlist'),
    url(r'^multicmd.html$', views.multi_cmd,name='multicmd'),
    url(r'^filehandler.html$', views.file_handler,name='filehandler'),
    url(r'^multitask.html$', views.multi_task,name='multitask'),
    url(r'^download.html$', views.download_file,name='download'),
    url(r'^taskresult.html$', views.task_result,name='taskresult'),
    url(r'^login.html$', views.user_login,name='login'),
    url(r'^token.html$', views.token,name='token'),
    url(r'^logout.html$', views.user_logout,name='logout'),
    url(r'^api/hostlist.html$', views.get_hosts),
]
