from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from .models import Report


class ReportsListView(LoginRequiredMixin, ListView):
    model = Report
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return super().get_queryset().filter(name__icontains=query)
