import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
from django.core.asgi import get_asgi_application
application = get_asgi_application()
