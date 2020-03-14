from django.urls import path
from django.views.generic import TemplateView

from base_app.views import InitialSettingView

app_name = 'base'

urlpatterns = [
    path('', TemplateView.as_view(template_name='base_app/base.html'), name='base'),
    path('text_base/', TemplateView.as_view(template_name='base_app/text_page_base.html'), name='index'),
    path('title/', InitialSettingView.as_view(), name='title'),
]
