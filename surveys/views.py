from django.views.generic import TemplateView

class listView(TemplateView):
    template_name = "base.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "質問一覧"
        return context