from django.urls import path
from . import views

app_name = 'ai_engine'

urlpatterns = [
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('tools/', views.ai_tools_dashboard, name='tools_dashboard'),
    path('tools/import-ocr/', views.add_ocr_items_to_cart, name='import_ocr'),
]
