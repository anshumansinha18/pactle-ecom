
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/user/", include("users.urls")),
    path("api/store/", include("store.urls")),
    path('admin/', admin.site.urls),
]
