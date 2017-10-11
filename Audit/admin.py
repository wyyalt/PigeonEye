from django.contrib import admin

from Audit import models

admin.site.register(models.Host)
admin.site.register(models.HostUser)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUserBind)
admin.site.register(models.Account)
admin.site.register(models.IDC)
admin.site.register(models.AuditLog)
admin.site.register(models.SessionLog)
admin.site.register(models.Token)
