"""
Enrutamiento raíz del proyecto.

- /admin/  : administración de Django (gestión del catálogo, Back-Office).
- /        : Portal del Cliente (app "portal").
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("portal.urls")),
]
