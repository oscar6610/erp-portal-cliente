"""Carga datos de prueba del Portal del Cliente.

Uso:
    python manage.py crear_datos_prueba
"""

from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from portal.models import Cliente, Producto


PRODUCTOS = [
    ("AUR-001", "Aural One", "Audio", "Nordica", "189990", 24,
     "Auriculares inalambricos de alta fidelidad con cancelacion adaptativa y 40 horas de bateria."),
    ("AUR-002", "Aural Pro", "Audio", "Nordica", "249990", 12,
     "Version profesional con drivers de 50 mm y estuche rigido."),
    ("AUR-003", "Pulse Buds", "Audio", "Tempo", "59990", 80,
     "Audifonos compactos con estuche de carga y resistencia al agua IPX4."),
    ("PAR-001", "Parlante Mesa", "Audio", "Tempo", "89990", 30,
     "Parlante bluetooth de escritorio con 20 W de potencia."),
    ("TEC-001", "Teclado Mecanico K7", "Perifericos", "Nordica", "74990", 45,
     "Teclado mecanico compacto con switches lineales y retroiluminacion."),
    ("TEC-002", "Mouse Ergo M2", "Perifericos", "Nordica", "39990", 60,
     "Mouse ergonomico inalambrico con sensor de 4000 dpi."),
    ("TEC-003", "Hub USB-C 7 en 1", "Perifericos", "Tempo", "34990", 100,
     "Adaptador multipuerto con HDMI, USB 3.0, lector SD y carga PD."),
    ("TEC-004", "Monitor 27 QHD", "Perifericos", "Tempo", "329990", 8,
     "Monitor de 27 pulgadas QHD con 165 Hz y cobertura sRGB del 99 por ciento."),
    ("HOG-001", "Lampara de Escritorio", "Hogar", "Nordica", "29990", 50,
     "Lampara LED regulable con brazo articulado y temperatura de color ajustable."),
    ("HOG-002", "Organizador Modular", "Hogar", "Tempo", "19990", 75,
     "Set de tres modulos apilables para escritorio."),
]

CLIENTES = [
    ("12345678-9", "Ana Perez", "ana.perez@example.com", "+56911111111",
     "Av. Siempre Viva 742, Santiago", "clave123"),
    ("98765432-1", "Bruno Diaz", "bruno.diaz@example.com", "+56922222222",
     "Calle Falsa 123, Chillan", "clave456"),
]


class Command(BaseCommand):
    help = "Crea productos y clientes de prueba para el prototipo"

    def handle(self, *args, **options):
        creados_p = 0
        for codigo, nombre, categoria, marca, precio, stock, descripcion in PRODUCTOS:
            _, creado = Producto.objects.get_or_create(
                codigo=codigo,
                defaults={
                    "nombre": nombre,
                    "categoria": categoria,
                    "marca": marca,
                    "precio": Decimal(precio),
                    "stock": stock,
                    "descripcion": descripcion,
                },
            )
            creados_p += int(creado)

        creados_c = 0
        for rut, nombre, correo, telefono, direccion, clave in CLIENTES:
            _, creado = Cliente.objects.get_or_create(
                rut=rut,
                defaults={
                    "nombre": nombre,
                    "correo": correo,
                    "telefono": telefono,
                    "direccion": direccion,
                    "password": make_password(clave),
                },
            )
            creados_c += int(creado)

        self.stdout.write(self.style.SUCCESS(
            f"Productos nuevos: {creados_p} (total {Producto.objects.count()}) | "
            f"Clientes nuevos: {creados_c} (total {Cliente.objects.count()})"
        ))
        self.stdout.write("Credenciales de prueba: 12345678-9 / clave123")
