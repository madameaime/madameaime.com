from django.views.generic import TemplateView

from braces.views import SuperuserRequiredMixin


class BackofficeIndexView(SuperuserRequiredMixin, TemplateView):
    template_name = 'mmm_backoffice/general/index.html'
