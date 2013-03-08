from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_mail(subject, mail_to, mail_from,
              template_text, template_html,
              params=None):
    text = render_to_string(template_text, params)
    html = render_to_string(template_html, params)

    msg = EmailMultiAlternatives(subject, text, mail_from, mail_to)
    msg.attach_alternative(html, 'text/html')
    msg.send()
