"""
WSGI config for UrSpace project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UrSpace.settings")

# 获取 Django WSGI 应用
application = get_wsgi_application()

# 添加 WhiteNoise 以提供静态文件
application = WhiteNoise(application)

