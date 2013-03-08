from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(needs_autoescape=True)
def nl2li(text, autoescape=None):
    """Wrap every line of `text` in a <li>.
    To understand how escaping is done, look Django documentation at:
    https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#filters-and-auto-escaping
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe('\n'.join('<li>%s</li>' % esc(line.strip())
                     for line in text.split('\n') if line))
