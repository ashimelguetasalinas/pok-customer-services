# POK - Sistema Inteligente de Atención al Cliente

## 1. Descripción
Este proyecto integra un backend Django Rest Framework y un frontend Nuxt 4 para gestionar mensajes de clientes y procesarlos con IA (OpenAI GPT).  
El sistema clasifica automáticamente los mensajes por categoría y sentimiento, y genera respuestas sugeridas.

---

## 2. Arquitectura
- **Backend**: Django + DRF  
  - Exposición de endpoints REST para consultas.
  - Lógica de IA separada en servicios.
  - Celery para procesamientos asíncronos.
  - Redis como broker para Celery.
  - Base de datos SQLite (persistente con volumen Docker).

- **Frontend**: Nuxt 3 + Vue 3  
  - Dashboard para visualizar consultas.
  - Vista de detalle con edición de respuesta sugerida.
  - Consumo de API vía variables de entorno.

- **Docker**: Multi-servicio  
  - Backend, Frontend, Redis, Celery y Flower.
  - Docker Compose central para levantar todo con un solo comando.

---

## 3. Instalación y ejecución

### Requisitos
- Docker y Docker Compose instalados
- Node.js y npm (solo para desarrollo frontend)

### Levantar todo con Docker
```bash
# Desde la raíz del proyecto
docker-compose up --build
