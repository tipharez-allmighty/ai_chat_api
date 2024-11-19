from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import system_prompt_view, ChatAPIView, ChatAPIViewTest

urlpatterns = [
    path('test_prompt/', system_prompt_view, name='system_prompt'),
    path('',ChatAPIView.as_view(), name='chat_api'),
    path('test/', ChatAPIViewTest.as_view(), name='api_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)