from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    #  This adds URL names: login, logout, password_change, etc.
    path("accounts/", include("django.contrib.auth.urls")),

    # Your app
    path("", include("bookings.urls")),
]