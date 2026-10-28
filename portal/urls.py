from django.urls import path

from . import views

app_name = "portal"

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("producto/<int:pk>/", views.ficha, name="ficha"),
    path("producto/<int:pk>/agregar/", views.agregar, name="agregar"),
    path("carrito/", views.carrito, name="carrito"),
    path("carrito/confirmar/", views.confirmar, name="confirmar"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
