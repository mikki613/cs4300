from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # REQUIRED for {% url 'login' %} and {% url 'logout' %}
    path("accounts/", include("django.contrib.auth.urls")),

    path("", include("bookings.urls")),
]