from django.urls import path
from django.views.generic import TemplateView

from base_app import views

app_name = 'base'

urlpatterns = [
    # for development
    path('base_check/', TemplateView.as_view(template_name='base_app/base.html'), name='base'),
    path('text_base_check/', TemplateView.as_view(template_name='base_app/text_part/text_page_base.html'),
         name='index'),
    # main
    path('title/', views.InitialSettingView.as_view(), name='title'),
    path('page/<int:page_num>', views.page_create, name='content_pages'),
    path('bad_end_page/<str:bad_end_name>', views.bad_end_page_create, name='bad_end_pages'),
    # status function
    path('status/', views.StatusView.as_view(), name='status'),
    # others
    path('quote/', TemplateView.as_view(template_name='base_app/quote.html'), name='quote'),
    path('about/', TemplateView.as_view(template_name='base_app/about.html'), name='about'),
]
