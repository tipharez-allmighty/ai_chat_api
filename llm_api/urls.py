from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import system_prompt_view, ChatAPIView

urlpatterns = [
    path('hui/', system_prompt_view, name='system_prompt'),
    path('',ChatAPIView.as_view(), name='chat_api')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)