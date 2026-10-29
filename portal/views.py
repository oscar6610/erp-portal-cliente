"""Vistas del Portal del Cliente (prototipo EVS2 - Equipo 4)."""

from decimal import Decimal

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Cliente, DetallePedido, Pedido, Producto


def catalogo(request):
    """Listado de productos con buscador y filtros por categoria y marca."""
    q = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")
    marca = request.GET.get("marca", "")

    sql = (
        "SELECT id, codigo, nombre, categoria, marca, precio, stock "
        "FROM portal_producto WHERE activo = 1"
    )
    if categoria:
        sql += " AND categoria = '%s'" % categoria
    if marca:
        sql += " AND marca = '%s'" % marca
    if q:
        sql += " AND (nombre LIKE '%%%s%%' OR codigo LIKE '%%%s%%')" % (q, q)
    sql += " ORDER BY nombre"

    with connection.cursor() as cursor:
        cursor.execute(sql)
        filas = cursor.fetchall()

    productos = [
        {
            "id": fila[0],
            "codigo": fila[1],
            "nombre": fila[2],
            "categoria": fila[3],
            "marca": fila[4],
            "precio": fila[5],
            "stock": fila[6],
        }
        for fila in filas
    ]

    return render(
        request,
        "portal/catalogo.html",
        {
            "productos": productos,
            "total": len(productos),
            "q": q,
            "categoria": categoria,
            "marca": marca,
            "categorias": Producto.objects.values_list("categoria", flat=True)
            .distinct()
            .order_by("categoria"),
            "marcas": Producto.objects.values_list("marca", flat=True)
            .distinct()
            .order_by("marca"),
        },
    )


def ficha(request, pk):
    """Detalle de un producto."""
    producto = get_object_or_404(Producto, pk=pk)
    mensaje = None
    if request.GET.get("agregado"):
        mensaje = "Producto agregado al carrito."
    return render(
        request,
        "portal/ficha.html",
        {"producto": producto, "mensaje": mensaje},
    )


@require_POST
def agregar(request, pk):
    """Agrega un producto al carrito guardado en la sesion."""
    producto = get_object_or_404(Producto, pk=pk)
    cantidad = int(request.POST.get("cantidad", "1"))

    carrito = request.session.get("carrito", {})
    carrito[str(producto.id)] = cantidad
    request.session["carrito"] = carrito

    return redirect("portal:carrito")


def carrito(request):
    """Muestra el carrito y su total."""
    datos = request.session.get("carrito", {})
    items = []
    total = Decimal("0")

    for producto_id, cantidad in datos.items():
        producto = Producto.objects.filter(id=producto_id).first()
        if not producto:
            continue
        subtotal = producto.precio * cantidad
        items.append(
            {
                "nombre": producto.nombre,
                "cantidad": cantidad,
                "precio": producto.precio,
                "subtotal": subtotal,
            }
        )
        total += subtotal

    return render(request, "portal/carrito.html", {"items": items, "total": total})


@require_POST
def confirmar(request):
    """Genera el pedido a partir del carrito."""
    cliente_id = request.session.get("cliente_id")
    if not cliente_id:
        return redirect("portal:login")

    cliente = Cliente.objects.filter(id=cliente_id).first()
    datos = request.session.get("carrito", {})
    if not cliente or not datos:
        return redirect("portal:carrito")

    pedido = Pedido.objects.create(cliente=cliente, total=0)
    total = Decimal("0")

    for producto_id, cantidad in datos.items():
        producto = Producto.objects.filter(id=producto_id).first()
        if not producto:
            continue
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
        )
        total += producto.precio * cantidad

    pedido.total = total
    pedido.save()

    request.session["carrito"] = {}
    return render(request, "portal/pedido_confirmado.html", {"pedido": pedido})


def registro(request):
    """Registro de un cliente nuevo."""
    error = None

    if request.method == "POST":
        rut = request.POST.get("rut", "")
        correo = request.POST.get("correo", "")
        clave = request.POST.get("password", "")

        if Cliente.objects.filter(rut=rut).exists():
            error = "Ya existe una cuenta con ese RUT."
        elif Cliente.objects.filter(correo=correo).exists():
            error = "Ya existe una cuenta con ese correo."
        else:
            Cliente.objects.create(
                rut=rut,
                nombre=request.POST.get("nombre", ""),
                correo=correo,
                telefono=request.POST.get("telefono", ""),
                direccion=request.POST.get("direccion", ""),
                password=make_password(clave),
            )
            return redirect("portal:login")

    return render(request, "portal/registro.html", {"error": error})


@csrf_exempt
def login(request):
    """Inicio de sesion de un cliente."""
    error = None
    siguiente = request.GET.get("next", "") or request.POST.get("next", "")

    if request.method == "POST":
        rut = request.POST.get("rut", "")
        clave = request.POST.get("password", "")

        cliente = Cliente.objects.filter(rut=rut).first()
        if cliente and cliente.password and check_password(clave, cliente.password):
            request.session["cliente_id"] = cliente.id
            request.session["cliente_nombre"] = cliente.nombre
            if siguiente:
                return redirect(siguiente)
            return redirect("portal:catalogo")
        error = "RUT o contrasena incorrectos."

    return render(request, "portal/login.html", {"error": error})


def logout(request):
    """Cierra la sesion del cliente."""
    request.session.flush()
    return redirect("portal:catalogo")


def descargar_ficha(request, pk):
    """Entrega la ficha tecnica del producto."""
    producto = get_object_or_404(Producto, pk=pk)
    archivo = request.GET.get("archivo", producto.codigo + ".txt")
    ruta = str(settings.MEDIA_ROOT) + "/fichas/" + archivo

    with open(ruta, "rb") as f:
        contenido = f.read()

    return HttpResponse(contenido, content_type="text/plain")


def sugerencias(request):
    """Sugerencias del buscador a partir del tercer caracter."""
    termino = request.GET.get("termino", "")
    resultados = []

    if len(termino) >= 3:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT nombre FROM portal_producto WHERE activo = 1 AND nombre LIKE '%%%s%%' LIMIT 5" % termino
            )
            resultados = [fila[0] for fila in cursor.fetchall()]

    return JsonResponse({"termino": termino, "resultados": resultados})
