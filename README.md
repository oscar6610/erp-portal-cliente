# ERP Portal del Cliente — Equipo 4

Prototipo funcional del módulo **Portal del Cliente (Ventas en línea)** del ERP
de Seguridad LTDA, desarrollado para la **Evaluación Sumativa 2** de la
asignatura Desarrollo Seguro (CI3064) — Unidad 2: Desarrollo y pruebas de
software seguro.

- Instancia de Jira: <https://oscararavena2018.atlassian.net/jira/software/projects/ERP/boards>
- Tablero del proyecto: proyecto `ERP` (Épica `ERP-1`)

## Stack

| Componente | Versión |
|---|---|
| Python | 3.14 |
| Django | 6.1.2 |
| MySQL | 8.x (driver PyMySQL) |
| Configuración | variables de entorno (.env) |

## Puesta en marcha

```bash
# 1. Entorno virtual e dependencias
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 2. Configuración local (no se versiona)
copy .env.example .env
#    generar la clave y pegarla en DJANGO_SECRET_KEY:
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"

# 3. Base de datos (crear la base y el usuario en MySQL antes de migrar)
python manage.py migrate

# 4. Ejecutar
python manage.py runserver
```

El portal queda disponible en <http://localhost:8000> y la administración en
<http://localhost:8000/admin/>.

## Estructura

```
config/            configuración del proyecto (settings, urls, wsgi)
portal/            aplicación del Portal del Cliente
  templates/       plantillas HTML
  urls.py          rutas del portal
  views.py         vistas
manage.py          utilidad de administración de Django
index.html         maqueta original del catálogo y ficha de producto
```

## Reglas de trabajo del equipo

1. La rama `main` está protegida: todo cambio entra por Pull Request con la
   aprobación de un compañero.
2. Cada commit lleva la clave del ticket de Jira (Smart Commit), por ejemplo:
   `ERP-25 #comment Configura settings con variables de entorno`.
3. Ninguna contraseña, token o llave se sube al repositorio: viven en `.env`.

## Estado

| Ticket | Alcance | Estado |
|---|---|---|
| ERP-25 | Base del proyecto Django + MySQL por variables de entorno | En curso |
| ERP-26 | Modelo de datos y migraciones | Pendiente |
| ERP-27 | Registro e inicio de sesión de clientes | Pendiente |
| ERP-28 | Catálogo por categoría y marca | Pendiente |
| ERP-29 | Buscador de productos | Pendiente |

> En esta etapa el prototipo se construye de forma natural, sin mecanismos de
> blindaje, para que el análisis estático de la Etapa 2 audite el código real
> del equipo. Los controles se planifican en el Sprint 2 de remediación.
