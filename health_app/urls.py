from django.urls import path
from .views import StepComparisonView,AIResultView

urlpatterns = [
    path('step-comparison/', StepComparisonView.as_view(), name='step-comparison'),
    path('ai-result/', AIResultView.as_view(), name='ai-result'),
]