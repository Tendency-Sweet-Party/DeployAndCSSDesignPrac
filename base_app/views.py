from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from base_app.forms import InitialSettingForm


class InitialSettingView(FormView):
    template_name = 'base_app/initial_setting.html'
    form_class = InitialSettingForm

    def post(self, request, *args, **kwargs):
        if request.POST.get('next', '') == 'create':
            form = InitialSettingForm(request.POST)
            if form.is_valid():
                # ctx = {}
                # セッションにデータを保存
                initial_setting_data = {
                    'main_character_name': form.cleaned_data['main_character_name'],
                    'special_move': form.cleaned_data['special_move'],
                    'job_after': form.cleaned_data['job_after'],
                    'state_of_progress': 1,
                }
                request.session['initial_setting_data'] = initial_setting_data
                # ctx['initial_setting_data'] = initial_setting_data
                return redirect(reverse('base:content_pages', kwargs={'page_num': 1, }))
            else:
                return render(request, self.template_name, {'form': form})
        else:
            return redirect(reverse_lazy('base:title'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['setting_component'] = ctx.pop('form')
        return ctx


def page_create(request, page_num):
    template_name = ''

    if not page_num:
        return HttpResponseForbidden('403 Forbidden', content_type='text/html')
    elif 'initial_setting_data' not in request.session:
        return HttpResponseForbidden('403 Forbidden', content_type='text/html')
    elif request.session['initial_setting_data']['state_of_progress'] < page_num:
        return HttpResponseForbidden('403 Forbidden', content_type='text/html')

    # 進行度をインクリメント
    request.session['initial_setting_data']['state_of_progress'] = request.session['initial_setting_data'].get(
        'state_of_progress', 0) + 1
    # contextを作成
    data = {
        'main_character_name': request.session['initial_setting_data']['main_character_name'],
        'special_move': request.session['initial_setting_data']['special_move'],
        'job_after': request.session['initial_setting_data']['job_after'],
        'state_of_progress': request.session['initial_setting_data']['state_of_progress'],
    }
    ctx = {'data': data}
    # template先を編集
    template_name = 'common_part_' + str(page_num) + '.html'

    return render(request, 'base_app/text_part/' + template_name, ctx)
