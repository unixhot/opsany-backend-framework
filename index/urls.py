from django.urls import path
from index.views import vue, healthz

urlpatterns = [
    path("", vue),
    path(r"healthz/", healthz),
]
