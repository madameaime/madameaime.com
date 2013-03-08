from django import template

from mmm.forms import NewsletterForm


register = template.Library()


@register.simple_tag
def newsletter_email_html_name():
    return NewsletterForm()['email'].html_name
