import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UrSpace.settings")

application = get_wsgi_application()
application = WhiteNoise(application)  # ✅ 让 WhiteNoise 自动查找 `STATIC_ROOT`
