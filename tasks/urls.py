from django.urls import path
from .views import tickets_page, suggest_tasks, analyze_tasks

urlpatterns = [
    path('analyze/', analyze_tasks, name='analyze_tasks'),
    path('suggest/', suggest_tasks, name='suggest_tasks'),
    path('tickets/', tickets_page, name='tickets'),
]
