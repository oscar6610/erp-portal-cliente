"""Vistas del Portal del Cliente (prototipo EVS2 — Equipo 4)."""

import django
from django.db import connection
from django.shortcuts import render


def home(request):
    """Página de inicio del portal: confirma que el proyecto está operativo."""
    return render(
        request,
        "portal/home.html",
        {
            "django_version": django.get_version(),
            "db_vendor": connection.vendor,
            "db_name": connection.settings_dict.get("NAME"),
        },
    )
