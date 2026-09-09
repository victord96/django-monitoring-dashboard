from django.urls import path
from .views import ScorecardView

urlpatterns = [
    path("", ScorecardView.as_view(), name="scorecard"),
]
