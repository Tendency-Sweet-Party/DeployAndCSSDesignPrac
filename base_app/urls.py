from django.urls import path
from django.views.generic import TemplateView

app_name = 'base'

urlpatterns = [
    path('', TemplateView.as_view(template_name='base_app/base.html'), name='base'),
    path('text_base/', TemplateView.as_view(template_name='base_app/text_page_base.html'), name='index'),
]
