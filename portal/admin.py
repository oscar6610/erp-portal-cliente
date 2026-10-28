from django.contrib import admin

from .models import Cliente, DetallePedido, Pedido, Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "categoria", "marca", "precio", "stock", "activo")
    list_filter = ("categoria", "marca", "activo")
    search_fields = ("codigo", "nombre")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre", "correo", "telefono")
    search_fields = ("rut", "nombre", "correo")


class DetalleInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "fecha", "estado", "total")
    list_filter = ("estado",)
    inlines = [DetalleInline]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "producto", "cantidad", "precio_unitario")
