from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from tasks.views import tickets_page   # 👈 add this import

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", TemplateView.as_view(template_name="index.html"), name="home"),

    path("api/tasks/", include("tasks.urls")),

    path("tickets/", tickets_page, name="tickets"),   # 👈 NEW
]
