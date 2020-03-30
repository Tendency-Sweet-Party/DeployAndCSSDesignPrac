import pprint

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from django.contrib.sessions.models import Session
from django.utils.safestring import mark_safe

from base_app.admin_actions import export_as_csv_action


@admin.register(Session)
class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return mark_safe(pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n'))

    def _session_property(self, obj, property_name):
        d = obj.get_decoded()
        initial_setting_data = d['initial_setting_data'] if 'initial_setting_data' in d else ''
        return initial_setting_data[property_name] if property_name in initial_setting_data else ''

    def _main_character_name(self, obj):
        return SessionAdmin._session_property(self, obj, 'main_character_name')

    def _special_move(self, obj):
        return SessionAdmin._session_property(self, obj, 'special_move')

    ITEMS = (
        'session_key',
        '_session_data',
        '_main_character_name',
        '_special_move',
        'expire_date',
    )

    DISPLAYED_ITEMS = (
        'session_key',
        '_main_character_name',
        '_special_move',
        'expire_date',
    )

    list_display = DISPLAYED_ITEMS
    list_display_links = DISPLAYED_ITEMS
    list_filter = (
        'session_key',
        'expire_date',
    )
    readonly_fields = ITEMS
    exclude = ('session_data',)
    ordering = ('-expire_date',)
    date_hierarchy = 'expire_date'

    actions = [export_as_csv_action('CSV Export', fields=ITEMS), ]
