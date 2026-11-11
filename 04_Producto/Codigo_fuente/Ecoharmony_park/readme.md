# EcoHarmony Park: Inscribirme a actividad

Implementación de la User Story **"Inscribirme a actividad"** del caso de estudio EcoHarmony Park, desarrollada con TDD para el **TP 6** de Ingeniería y Calidad de Software (UTN FRC, 4K2, Grupo 2).

> **COMO** visitante **QUIERO** inscribirme a una actividad **PARA** reservar mi lugar en la misma.

Las reglas de negocio que el enunciado no definía están en [`tp6_aclaraciones_us.md`](../../../03_Entregas/TPs/TP_6/Entrega/tp6_aclaraciones_us.md).

## Stack

| Capa | Tecnología |
|------|------------|
| Backend y API | Python 3.13, Django 6.1, Django REST Framework |
| Base de datos | PostgreSQL 17 |
| Tareas en segundo plano | Celery 5.6 con Redis 7 como cola |
| Front | Templates de Django, CSS propio y JavaScript que consume la API con `fetch` |
| Dependencias | [uv](https://docs.astral.sh/uv/) |
| Entorno | Docker Compose |

## Requisitos

- **Docker** con **Docker Compose**. Son obligatorios: la base, la cola, la API y el worker corren en contenedores.
- **uv**, solo si querés correr los tests o comandos fuera de Docker.

## Puesta en marcha

Todos los comandos se corren **desde esta carpeta** (`04_Producto/Codigo_fuente/Ecoharmony_park/`).

### 1. Variables de entorno

```bash
cp .env.example .env
```

Completá el `.env`:

| Variable | Para qué sirve |
|----------|----------------|
| `DJANGO_SECRET_KEY` | Clave de Django. Obligatoria. |
| `DJANGO_DEBUG` | **Tiene que ser `True`**: el servidor de desarrollo solo sirve el CSS y el JS con `DEBUG` activo. |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por coma. Con `DEBUG=True` y vacío acepta `localhost`. |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Base de datos. Las usan el contenedor de PostgreSQL y Django. |
| `POSTGRES_HOST`, `POSTGRES_PORT` | Dónde está la base cuando Django corre fuera de Docker. En Docker se usan `db` y `5432` automáticamente. |
| `API_PORT` | Puerto del host donde se publica la aplicación (por defecto `8000`). |
| `CELERY_BROKER_URL` | Redis para correr fuera de Docker. En Docker se usa `redis://redis:6379/0` automáticamente. |
| `DJANGO_EMAIL_SMTP` | `True` envía mails reales por SMTP; `False` los imprime en el log del worker. |
| `DJANGO_EMAIL_HOST_USER`, `DJANGO_EMAIL_HOST_PASSWORD` | Cuenta de Gmail y su **contraseña de aplicación** (no la contraseña de la cuenta). Se genera en https://myaccount.google.com/apppasswords con la verificación en 2 pasos activa. |
| `DJANGO_DEFAULT_FROM_EMAIL` | Remitente de los mails. Tiene que ser la misma cuenta de Gmail. |

### 2. Levantar los servicios

```bash
docker compose up -d --build
```

| Servicio | Qué hace |
|----------|----------|
| `db` | PostgreSQL. |
| `redis` | Cola de mensajes de Celery. Solo es accesible dentro de la red de Docker. |
| `api` | Aplica las migraciones y levanta Django en `http://localhost:${API_PORT}`. |
| `worker` | Worker de Celery: envía los mails de confirmación. |

### 3. Cargar los datos de prueba

```bash
docker compose exec api python manage.py seed --email tu_mail@gmail.com
```

Crea el usuario de prueba, las cuatro actividades y sus horarios para los próximos 30 días (`--dias` para cambiarlo). Se puede correr las veces que haga falta: no duplica datos.

| Usuario | Contraseña |
|---------|------------|
| `visitante` | `visitante1234` |

Para entrar al admin de Django (`/admin/`) y gestionar actividades y horarios:

```bash
docker compose exec api python manage.py createsuperuser
```

### 4. Usarla

Entrá a `http://localhost:${API_PORT}`, ingresá con el usuario de prueba y reservá una actividad. El pase aparece al instante y el mail con el código QR llega unos segundos después, enviado por el worker.

## Tests

```bash
docker compose exec api python manage.py test
```

Fuera de Docker, con la base levantada (`docker compose up -d db`):

```bash
uv run python manage.py test
```

Los tests no necesitan Redis: el test runner (`core/test_runner.py`) ejecuta las tareas de Celery en el momento.

Cobertura (configurada en `pyproject.toml`; excluye migraciones y los propios tests):

```bash
docker compose exec api sh -c "coverage run manage.py test && coverage report"
# o fuera de Docker:
uv run coverage run manage.py test && uv run coverage report
uv run coverage html                # reporte navegable en htmlcov/index.html
```

| Nivel | Tipo de test | Qué prueba |
|-------|--------------|------------|
| Reglas de negocio | `SimpleTestCase` con dobles en memoria | `InscripcionService`, `DisponibilidadService`, calendario del parque, serializer |
| Acceso a datos | `TestCase` sobre PostgreSQL | Repositorios, conteos en una sola query, transacción y bloqueo |
| Concurrencia | `TransactionTestCase` con hilos | Dos inscripciones simultáneas no superan el último cupo |
| Mail y tareas | `TestCase` | Contenido del mail, QR embebido, encolado y reintentos de Celery |
| Aceptación | `APITestCase` | Las pruebas de usuario PU1 a PU6 de punta a punta por HTTP |

## Arquitectura

Arquitectura por capas: **View → Service → Repository**. Las vistas solo coordinan HTTP, los servicios tienen las reglas de negocio y los repositorios el acceso a datos. Un servicio nunca usa el repositorio de otro dominio: lo consulta a través de su servicio.

```
apps/
├── usuarios/        Usuario con email único (destino del mail de confirmación)
├── actividades/     Actividades, horarios, calendario del parque y comando seed
└── inscripciones/   Inscripción, participantes, disponibilidad, notificación y tarea de Celery
core/                Settings, URLs, Celery, exception handler y test runner
front/               Templates, CSS y JS de las páginas (las apps solo tienen la API)
```

### API

Todos los endpoints requieren sesión iniciada.

| Método | Ruta | Devuelve |
|--------|------|----------|
| `GET` | `/api/actividades/` | Actividades activas |
| `GET` | `/api/horarios-disponibles/?actividad_id=` | Horarios futuros, con el parque abierto y cupo, con sus lugares libres |
| `POST` | `/api/inscripciones/` | La inscripción creada (201) o el error con formato `{"codigo", "detalle", "errores"}` |

### Envío del mail

```
POST /api/inscripciones/ ─► InscripcionService ─► guarda la inscripción ─► ColaNotificador ─► Redis
                                                                                                │
         la respuesta vuelve al instante ◄─────────────────────────────────────────────────────┘
                                                                                                ▼
                                                    worker de Celery ─► EmailNotificador ─► SMTP
```

Si el SMTP falla, la tarea se reintenta hasta 3 veces con espera creciente. Si Redis no responde, la inscripción igual se confirma y el error queda en el log.

## Comandos útiles

```bash
docker compose logs -f worker      # ver los mails que se envían (o se imprimen, con SMTP apagado)
docker compose logs -f api         # ver las peticiones y errores de la API
docker compose down                # apagar todo (los datos de la base se conservan)
```
