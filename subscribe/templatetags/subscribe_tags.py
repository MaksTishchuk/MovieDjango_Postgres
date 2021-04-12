from django import template
from subscribe.forms import SubscribeForm

register = template.Library()


@register.inclusion_tag('subscribe/tags/form.html')
def subsribe_form():
    return {'subscribe_form': SubscribeForm()}
