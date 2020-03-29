from django import template

from DeployAndCSSDesignPrac import settings

register = template.Library()


@register.simple_tag
def show_site_title():
    return settings.SITE_TITLE


@register.simple_tag
def show_site_version():
    return settings.SITE_VERSION
