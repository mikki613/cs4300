from django.contrib import admin
from django.urls import include, path

from bookings import views as booking_views


urlpatterns = [
    path("admin/", admin.site.urls),

    # HTML pages
    path("", include("bookings.urls")),

    # Auth
    path("accounts/signup/", booking_views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
]