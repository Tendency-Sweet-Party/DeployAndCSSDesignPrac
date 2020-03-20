from django.urls import path
from django.views.generic import TemplateView

from base_app import views

app_name = 'base'

urlpatterns = [
    # todo for development
    path('', TemplateView.as_view(template_name='base_app/base.html'), name='base'),
    path('text_base/', TemplateView.as_view(template_name='base_app/text_part/text_page_base.html'), name='index'),
    # main
    path('title/', views.InitialSettingView.as_view(), name='title'),
    path('page/<int:page_num>', views.page_create, name='content_pages'),
    path('quote/', TemplateView.as_view(template_name='base_app/quote.html'), name='quote'),
    # status function
    path('status/', views.StatusView.as_view(), name='status'),
]
