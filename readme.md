# POK - Sistema Inteligente de Atención al Cliente

## 1. Descripción
Este proyecto integra un **backend Django Rest Framework** y un **frontend Nuxt 3 / Vue 3** para gestionar mensajes de clientes y procesarlos automáticamente con **IA (OpenAI GPT)**.  

El sistema clasifica los mensajes por categoría y sentimiento, y genera **respuestas sugeridas** editables. Está pensado para mejorar la productividad de los equipos de atención al cliente en POK.

---

## 2. Arquitectura General

flowchart LR
    A[Cliente / Lead] -->|Envía mensaje| B[Frontend Nuxt 3]
    B -->|POST /api/inquiries| C[Backend Django DRF]
    C -->|Procesamiento asíncrono| D[Celery Worker]
    D -->|Llama a OpenAI GPT| E[OpenAI API]
    E -->|Resultado JSON| D
    D --> C
    C -->|GET /api/inquiries| B


## 3. Detalles
    Backend:
    Django + DRF para endpoints RESTful
    Lógica de IA separada en servicios (services/openai_service.py)
    Celery para procesamiento asíncrono (no bloquea requests)
    Redis como broker
    SQLite como DB persistente (volumen Docker)
    Manejo de errores robusto (API fallida, JSON mal formado, etc.)
    --------------------------------------------------------------
    Frontend:
    Nuxt 3 + Vue 3
    Dashboard con lista de consultas y filtros
    Indicadores visuales (colores/badges) según categoría y sentimiento
    Vista de detalle con respuesta sugerida editable
    Consumo de API mediante variable de entorno (NUXT_PUBLIC_API_URL)
    Docker / DevOps
    Dockerfiles separados por proyecto (backend / frontend)
    Docker Compose central para levantar todo el stack
    Persistencia de SQLite mediante volúmenes
    Flower para monitoreo de Celery

## 4. Instalación y Ejecución
    Requisitos
    Docker y Docker Compose
    Node.js y npm (solo para desarrollo frontend)
    Levantar todo con Docker
    bash
    Copiar código
    # Desde la raíz del proyecto
    docker-compose up --build
    Backend: http://localhost:8000
    Frontend: http://localhost:3000
    Flower (monitor Celery): http://localhost:5555

    Variables de entorno
    Backend (backend/customer_service_backend/.env):

    env
    DJANGO_SECRET_KEY=tu_clave
    DJANGO_DEBUG=1
    REDIS_URL=redis://redis:6379/0
    OPENAI_API_KEY=tu_api_key
    Frontend (pok-frontend/.env):

    env
    NUXT_PUBLIC_API_URL=http://web:8000/api

# 5. Endpoints principales

    Método	    Endpoint	                Descripción
    POST	/api/inquiries/create	    Crear una nueva consulta de cliente
    GET	    /api/inquiries/	            Listar todas las consultas
    GET	    /api/inquiries/{id}/	    Ver detalle de una consulta (incluye respuesta IA)

    Ejemplo de POST
    POST /api/inquiries/create
    Content-Type: application/json

    {
    "customer_name": "Juan Perez",
    "email": "juan@example.com",
    "message": "Tengo un problema con mi pedido"
    }

    Respuesta ejemplo:    
    {
    "id": 1,
    "customer_name": "Juan Perez",
    "email": "juan@example.com",
    "message": "Tengo un problema con mi pedido",
    "category": "Soporte Técnico",
    "sentiment": "Negativo",
    "suggested_reply": "Hola Juan, lamentamos el inconveniente. Nuestro equipo lo revisará y te contactará pronto."
    }

# 6. Features implementadas

    Recepción de consultas de clientes
    Clasificación automática por categoría y sentimiento (IA)
    Respuestas sugeridas editables en frontend
    Dashboard con indicadores visuales
    Procesamiento asíncrono con Celery + Redis
    Dockerizado todo el stack para desarrollo y producción
    Manejo de errores robusto (API OpenAI, JSON inválido)
    Monitoreo de tareas con Flower
    Persistencia de datos en SQLite mediante volúmenes Docker

# 7. Decisiones de Arquitectura
    Separación de responsabilidades: lógica de IA en services/, vistas limpias en backend, frontend solo consume API.
    Dockerización: cada proyecto tiene su Dockerfile (frontend / backend) y un docker-compose central para levantar todo.
    Persistencia de SQLite: usando volúmenes para no perder datos al reiniciar contenedores.
    Celery + Redis: procesamiento de IA asíncrono, evita bloquear requests HTTP.
    Nuxt 3 SSR: frontend moderno, rápido, con soporte de edición de respuestas y dashboard interactivo.

# 8. Bonus / Extra
    Ready para testing: puedes agregar pytest para backend y Vitest para frontend.
    Tipado completo: Python con type hints, frontend con TypeScript (opcional).
    Escalable: backend puede migrar a Postgres si se desea, frontend soporta SSR y SPA.