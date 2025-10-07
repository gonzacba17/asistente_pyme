# 🧾 Asistente Legal / Fiscal para PyMEs

Plataforma inteligente para automatizar tareas contables, fiscales y legales de pequeñas y medianas empresas.  
El sistema permite **gestionar comprobantes**, **recordar vencimientos AFIP**, **emitir reportes financieros** y **consultar asistencia legal automatizada**, integrando IA, OCR y visualización de datos con Power BI.

---

## 🚀 Objetivo General

Brindar a las PyMEs una herramienta **simple, eficiente y moderna** que reduzca la carga administrativa, mejore la gestión contable y minimice errores fiscales, automatizando tareas repetitivas y centralizando la información financiera.

---

## 🧠 Funcionalidades Principales (MVP y futuro desarrollo)

### 🧩 Módulo Contable / Fiscal
- Carga automática de facturas y comprobantes.
- Lectura OCR con **Tesseract** para extraer datos clave (fecha, CUIT, importe, vencimiento).
- Control y registro de vencimientos AFIP e impuestos.
- Generación de reportes básicos desde el backend (PDF / CSV).
- Integración con **Power BI Embedded** para visualizaciones interactivas.

### 👥 Gestión de Usuarios
- Registro e inicio de sesión de usuarios (JWT).
- Roles: administrador / contador / empresa.
- Panel de control personalizable.

### 🧾 Módulo de Comprobantes
- Subida de facturas o recibos en formato imagen o PDF.
- Almacenamiento en PostgreSQL con texto OCR indexado.
- Dashboard con próximos vencimientos y estados de facturas.

### 🤖 Asistente Legal (Futuro módulo)
- Chatbot legal integrado con modelo de lenguaje externo (IA).
- Consultas rápidas sobre temas impositivos o legales.

---

## 🧱 Arquitectura del Proyecto

El proyecto se compone de **4 servicios principales**, orquestados mediante Docker Compose.

/asistente_pyme/
├── backend/ → API principal (FastAPI - Python)
│ ├── app/
│ ├── tests/
│ ├── Dockerfile
│ └── requirements.txt
│
├── frontend/ → Interfaz web (React + Vite + Tailwind)
│ ├── src/
│ ├── package.json
│ └── Dockerfile
│
├── ocr_service/ → Microservicio OCR (Flask + Tesseract)
│ ├── app.py
│ └── Dockerfile
│
├── docker-compose.yml → Orquestación de servicios (profile: pyme)
└── README.md

yaml
Copiar código

---

## ⚙️ Tecnologías Utilizadas

| Área | Tecnología | Descripción |
|------|-------------|-------------|
| **Backend** | FastAPI (Python 3.11) | Framework rápido y moderno para APIs. |
| **Base de datos** | PostgreSQL | Base de datos relacional robusta. |
| **Frontend** | React + Vite + Tailwind | Interfaz moderna, ligera y responsiva. |
| **OCR** | Flask + Tesseract OCR | Lectura automática de comprobantes (PDF, imagen). |
| **Reportes** | Power BI Embedded | Visualización y análisis financiero. |
| **Contenedores** | Docker + Docker Compose | Despliegue simplificado multi-servicio. |

---

## 🧩 Estructura General del Sistema

```plaintext
+------------------------+
|        FRONTEND        | React + Tailwind (login, dashboard)
+-----------+------------+
            |
            v
+------------------------+
|        BACKEND         | FastAPI (auth, comprobantes, vencimientos)
+-----------+------------+
            |
            v
+------------------------+
|     OCR SERVICE        | Flask + Tesseract (lectura de facturas)
+-----------+------------+
            |
            v
+------------------------+
|     DATABASE (DB)      | PostgreSQL
+------------------------+
🔧 Requerimientos Previos
Docker Desktop instalado y en ejecución

Node.js (v18+)

Python (3.11+)

Visual Studio Code con extensiones recomendadas:

Python

Docker

Tailwind CSS IntelliSense

Prettier

ESLint

🧱 Instalación y Ejecución del Proyecto
Clonar el repositorio:

bash
Copiar código
git clone https://github.com/<tu_usuario>/asistente_pyme.git
cd asistente_pyme
Levantar todos los servicios con Docker:

bash
Copiar código
docker-compose --profile pyme up --build
Acceder a los servicios:

Backend (API): http://localhost:8000/docs

Frontend (Web): http://localhost:3000

OCR Service: http://localhost:5000

PostgreSQL: en puerto 5432

🧾 API Principales (MVP)
Método	Endpoint	Descripción
POST	/auth/register	Crear usuario
POST	/auth/login	Iniciar sesión
POST	/comprobantes/upload	Subir comprobante (con OCR)
GET	/comprobantes/	Listar comprobantes
GET	/comprobantes/vencimientos	Dashboard de vencimientos

💡 Ejemplo de Uso del OCR
Request:

bash
Copiar código
curl -X POST "http://localhost:8000/comprobantes/upload" \
  -F "file=@C:/Users/gonza/factura_test.jpg"
Response:

json
Copiar código
{
  "filename": "factura_test.jpg",
  "ocr_text": "Factura A - CUIT 30-12345678-9 - Total: $15000"
}
📊 Roadmap del Proyecto
Fase	Descripción	Estado
Fase 1 (MVP)	Backend FastAPI + OCR + DB + Frontend básico	✅ En desarrollo
Fase 2	Autenticación JWT, roles y permisos	⏳
Fase 3	Dashboard con Power BI Embedded	⏳
Fase 4	Asistente legal (chatbot IA)	🔜
Fase 5	Deploy en la nube (Render / AWS / Railway)	🔜

🧩 Scripts útiles
bash
Copiar código
# Levantar todos los servicios
docker-compose --profile pyme up --build

# Apagar contenedores
docker-compose down

# Ver logs
docker-compose logs -f backend
🧠 Futuras Mejoras
Integración directa con AFIP (API de comprobantes electrónicos)

Extracción automática de fechas de vencimiento

Integración con Gmail / Outlook para notificaciones

Chatbot legal con IA (modelos de lenguaje externo)

Categorización automática de gastos e ingresos

Exportación PDF / Excel de reportes

⭐ Cómo Contribuir
Haz un fork del repositorio

Crea una nueva rama: git checkout -b feature/nueva-funcionalidad

Haz commit de tus cambios

Envia un Pull Request 🚀

📎 Notas finales
El Asistente Legal/Fiscal para PyMEs busca ser una herramienta que simplifique la vida contable de los emprendedores y profesionales, aplicando automatización, inteligencia artificial y accesibilidad, con una arquitectura modular y escalable.

