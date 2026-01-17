# POK - Sistema Inteligente de Atención al Cliente

## 1. Descripción
Este proyecto implementa una solución completa para la gestión y clasificación inteligente de mensajes de atención al cliente. Utiliza una arquitectura de **microservicios** con **Django Rest Framework** como backend principal, **Nuxt 3** para el frontend, y un **microservicio FastAPI** dedicado exclusivamente a la Inteligencia Artificial.

El sistema recibe consultas, las envía a una cola de procesamiento (Celery), y utiliza el servicio de IA para clasificar el mensaje (Categoría, Sentimiento) y generar una respuesta sugerida profesional.

---

## 2. Arquitectura del Sistema

```mermaid
flowchart LR
    Client[Cliente / Frontend] -->|HTTP POST| Django[Backend Django]
    Django -->|Tarea Async| Celery[Celery Worker]
    Celery -->|HTTP Client| AI[Microservicio IA (FastAPI)]
    AI -->|OpenAI API| GPT[GPT-4o-mini]
    GPT --> AI
    AI --> Celery
    Celery -->|Actualiza DB| Postgres[PostgreSQL]
    Django -->|Lee Datos| Postgres
```

### Componentes:
- **Frontend**: Nuxt 3 + Vue 3 + TailwindCSS. Diseño moderno tipo Dashboard.
- **Backend Principal**: Django 5 + DRF. Maneja la lógica de negocio, usuarios y persistencia.
- **Microservicio IA**: FastAPI. Encapsula la lógica de interacción con OpenAI.
- **Cola de Tareas**: Celery + Redis. Asegura que el procesamiento de IA no bloquee la respuesta HTTP al usuario.
- **Base de Datos**: **PostgreSQL** (Dockerizada y conectada via red interna).
- **Documentación API**: DRF Spectacular (Swagger/Redoc).

---

## 3. Instalación y Ejecución

El proyecto está totalmente dockerizado para facilitar el despliegue.

### Requisitos
- Docker Desktop instalado.

### Pasos
1.  **Clonar el repositorio**:
    ```bash
    git clone <repo-url>
    cd customer_service_backend
    ```

2.  **Configurar Variables de Entorno**:
    Asegúrate de tener el archivo `backend/customer_service_backend/.env` con tu API Key de OpenAI:
    ```env
    OPENAI_API_KEY=sk-...
    DJANGO_DEBUG=1
    DJANGO_SECRET_KEY=secret
    CELERY_BROKER_URL=redis://redis:6379/0
    ```

3.  **Levantar el stack**:
    ```bash
    docker-compose up --build
    ```

4.  **Acceder a los servicios**:
    - **Frontend**: [http://localhost:3000](http://localhost:3000)
    - **Backend API**: [http://localhost:8000/api/](http://localhost:8000/api/)
    - **Swagger Docs**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
    - **Flower (Monitor Celery)**: [http://localhost:5555](http://localhost:5555)

---

## 4. Features Implementadas

### Backend
- ✅ **API RESTful** con Django Rest Framework.
- ✅ **Procesamiento Asíncrono** con Celery.
- ✅ **Microservicio Desacoplado** de IA con FastAPI.
- ✅ **Documentación Automática** con Swagger (OpenAPI 3.0).
- ✅ **Robustez**: Manejo de errores en llamadas a IA y reintentos automáticos.

### Frontend
- ✅ **Dashboard Moderno**: Vista de tarjetas (Grid) con indicadores visuales de estado.
- ✅ **Formulario de Creación**: Interfaz limpia para ingresar nuevas consultas.
- ✅ **Skeleton Loaders**: Mejor experiencia de usuario durante la carga de datos.
- ✅ **Modo Oscuro**: Soporte nativo para Dark Mode.
- ✅ **Feedback en Tiempo Real**: Polling para actualizar el estado del ticket (Pending -> Processed).

---

## 5. Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/inquiries/create/` | Crear nueva consulta. Desencadena tarea de IA. |
| GET | `/api/inquiries/` | Listar todas las consultas. |
| GET | `/api/inquiries/{id}/` | Ver detalle y respuesta sugerida. |

---

## 6. Decisiones de Diseño (Bonus)

- **Desacoplamiento total de IA**: Se extrajo la lógica de OpenAI a su propio servicio (`backend/ai_service`). Esto permite escalar la IA independientemente del backend principal o cambiar el proveedor de IA sin tocar el núcleo de Django.
- **Interacción HTTP**: El backend Django actúa como un cliente HTTP que consume el servicio de IA, simulando una arquitectura real de microservicios.
- **Type Safety**: Uso de Type Hints en Python y TypeScript en el Frontend para reducir errores en tiempo de desarrollo.
- **UX Premium**: Se priorizó una interfaz limpia y "app-like" en lugar de tablas administrativas estándar.