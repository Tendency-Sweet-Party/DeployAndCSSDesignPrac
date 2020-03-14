from django.shortcuts import render
from django.views.generic import FormView

from base_app.forms import InitialSettingForm


class InitialSettingView(FormView):
    template_name = 'base_app/initial_setting.html'
    form_class = InitialSettingForm
