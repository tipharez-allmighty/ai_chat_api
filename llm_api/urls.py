from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import system_prompt_view

urlpatterns = [
    path('', system_prompt_view, name='system_prompt'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)