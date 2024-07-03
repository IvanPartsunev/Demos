from django.core.cache import cache
from django.views.generic import TemplateView


class DataView(TemplateView):
    template_name = "beat-data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = cache.get("api_data", [])
        return context

