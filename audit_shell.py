
import sys
import os
from Audit.backend import user_interactive

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PigeonEye.settings")
    import django
    django.setup() #手动注册django所有app

    obj = user_interactive.UserShell(sys.argv)
    obj.start()