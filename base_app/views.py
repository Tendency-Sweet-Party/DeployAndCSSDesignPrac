from django.http import Http404
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.urls import reverse_lazy, reverse
from django.views.defaults import permission_denied
from django.views.generic import FormView, TemplateView

from base_app.const import status_dict
from base_app.forms import InitialSettingForm

ANNOUNCE_FOR_FORBIDDEN_PAGE = 'このページはまだ開けません。'
ANNOUNCE_FOR_NOT_FOUND = '存在しないページです。'


class InitialSettingView(FormView):
    template_name = 'base_app/initial_setting.html'
    form_class = InitialSettingForm

    def get(self, request, *args, **kwargs):
        is_reset = request.GET.get('reset')
        # セッション削除
        if is_reset == 'True':
            request.session.clear()
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('next', '') == 'create':
            form = InitialSettingForm(request.POST)
            if form.is_valid():
                # セッションにデータを保存
                initial_setting_data = {
                    'main_character_name': form.cleaned_data['main_character_name'],
                    'special_move': form.cleaned_data['special_move'],
                    'job_after': form.cleaned_data['job_after'],
                    'state_of_progress': 0,
                    'route_flag': '',
                }
                request.session['initial_setting_data'] = initial_setting_data
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
    if not page_num:
        return permission_denied(request, ANNOUNCE_FOR_FORBIDDEN_PAGE)
    elif 'initial_setting_data' not in request.session:
        return permission_denied(request, ANNOUNCE_FOR_FORBIDDEN_PAGE)
    elif request.session['initial_setting_data']['state_of_progress'] < (page_num - 1):
        return permission_denied(request, ANNOUNCE_FOR_FORBIDDEN_PAGE)

    # 次に進んだ場合は進行度を増やす
    if request.session['initial_setting_data']['state_of_progress'] < page_num:
        request.session['initial_setting_data']['state_of_progress'] = page_num

    # contextを作成
    data = {
        'main_character_name': request.session['initial_setting_data']['main_character_name'],
        'special_move': request.session['initial_setting_data']['special_move'],
        'job_after': request.session['initial_setting_data']['job_after'],
        'state_of_progress': request.session['initial_setting_data']['state_of_progress'],
    }
    ctx = {'data': data}
    # template名を編集
    template_name = 'common_part_' + str(page_num) + '.html'

    page_exist = True
    try:
        return render(request, 'base_app/text_part/' + template_name, ctx)
    except TemplateDoesNotExist:
        page_exist = False
        raise Http404(ANNOUNCE_FOR_NOT_FOUND)
    finally:
        if page_exist:
            # 変更を確定　
            # ※ https://djangoproject.jp/doc/ja/1.0/topics/http/sessions.html#id11
            request.session.modified = True


class StatusView(TemplateView):
    template_name = 'base_app/status_part/status.html'

    def get(self, request, *args, **kwargs):
        ctx = super(StatusView, self).get_context_data(**kwargs)
        if not request.session['initial_setting_data']:
            raise Http404(ANNOUNCE_FOR_NOT_FOUND)
        if request.session['initial_setting_data']['route_flag'] != '':
            raise Http404(ANNOUNCE_FOR_NOT_FOUND)
        if str(request.session['initial_setting_data']['state_of_progress']) not in status_dict:
            raise Http404(ANNOUNCE_FOR_NOT_FOUND)

        # ステータスデータ取得
        status_data = status_dict[
            str(request.session['initial_setting_data']['state_of_progress'])
        ]
        # 得意技を取得
        if request.session['initial_setting_data']['special_move']:
            if request.session['initial_setting_data']['special_move'] not in status_data['skill']:
                status_data['skill'].insert(0, request.session['initial_setting_data']['special_move'])

        ctx['status_data'] = status_data
        # contextを追加
        data = {
            'main_character_name': request.session['initial_setting_data']['main_character_name'],
            'special_move': request.session['initial_setting_data']['special_move'],
            'job_after': request.session['initial_setting_data']['job_after'],
        }
        ctx['data'] = data
        return self.render_to_response(ctx)
