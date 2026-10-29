"""Pruebas del Portal del Cliente."""

from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.test import TestCase

from .models import Cliente, Producto


class PortalTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            codigo="TST-001",
            nombre="Producto de prueba",
            categoria="Pruebas",
            marca="Marca",
            precio=1000,
            stock=10,
        )
        self.cliente = Cliente.objects.create(
            rut="11111111-1",
            nombre="Cliente Prueba",
            correo="prueba@example.com",
            password=make_password("clave-prueba"),
        )

    def test_catalogo_responde(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Catálogo")

    def test_busqueda_filtra_por_nombre(self):
        respuesta = self.client.get("/", {"q": "prueba"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["total"], 1)

    def test_login_con_credenciales_correctas(self):
        respuesta = self.client.post(
            "/login/", {"rut": "11111111-1", "password": "clave-prueba"}
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(self.client.session.get("cliente_id"), self.cliente.id)

    def test_login_con_credenciales_incorrectas(self):
        respuesta = self.client.post(
            "/login/", {"rut": "11111111-1", "password": "mala"}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsNone(self.client.session.get("cliente_id"))

    def test_carrito_suma_cantidades(self):
        self.client.post(
            "/producto/%s/agregar/" % self.producto.id, {"cantidad": "3"}
        )
        respuesta = self.client.get("/carrito/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["total"], Decimal("3000.00"))

    def test_sugerencias_devuelve_json(self):
        respuesta = self.client.get("/sugerencias/", {"termino": "produc"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["resultados"], ["Producto de prueba"])
