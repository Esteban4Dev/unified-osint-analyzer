# 🛰️ OSINT Dashboard

Plataforma que centraliza consultas OSINT (Shodan, VirusTotal, HaveIBeenPwned,
SecurityTrails, y reconocimiento DNS propio) en un solo dashboard.

Este proyecto corre **localmente sin Docker**: backend con un entorno virtual
de Python y frontend con `npm` directo. Interfaz y mensajes de error
disponibles en **español e inglés**.

## Estado de las fuentes

| Fuente | Estado | Notas |
|---|---|---|
| Shodan | ✅ Funcional | Requiere `SHODAN_API_KEY` (tier gratis disponible) |
| VirusTotal | ✅ Funcional | Requiere `VIRUSTOTAL_API_KEY` (tier gratis disponible) |
| DNS (reemplaza DNS Dumpster) | ✅ Funcional, sin key | DNS Dumpster no tiene API pública oficial, así que se hace reconocimiento DNS propio (A, AAAA, MX, NS, TXT, CNAME) |
| HaveIBeenPwned | 🟡 Listo, sin key | Requiere `HIBP_API_KEY` de pago |
| SecurityTrails | 🟡 Listo, sin key | Requiere `SECURITYTRAILS_API_KEY` (tier gratis limitado) |

Las fuentes sin key configurada simplemente devuelven
`{"configured": false, "error": "..."}` en vez de fallar — el dashboard
sigue funcionando con las que sí tengas activas.

## Idioma (Español / English)

- El selector **ES / EN** está en la barra de navegación superior.
- La preferencia se guarda en el navegador (`localStorage`), así que se
  mantiene entre sesiones.
- Al abrir la app por primera vez, se detecta automáticamente el idioma
  del navegador (si es español o inglés; si no, cae a español por defecto).
- La traducción cubre **toda la interfaz** (textos, botones, navegación) y
  también **los mensajes de error que vienen del backend** (por ejemplo
  "SHODAN_API_KEY no configurada" / "SHODAN_API_KEY not configured"),
  porque el frontend envía el idioma actual en cada búsqueda
  (`POST /api/osint/search {"query": "...", "lang": "es" | "en"}`).
- Para agregar un tercer idioma: añade sus textos en
  `frontend/src/i18n/translations.js` y en `backend/app/core/i18n.py`,
  y súmalo a `LANGUAGES` en el frontend.

## Requisitos previos

- Python 3.10+
- Node.js 18+ y npm

## Instalación

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `backend/.env` y pon tus claves reales de Shodan y VirusTotal:

```
SHODAN_API_KEY=tu_key_real
VIRUSTOTAL_API_KEY=tu_key_real
```

Levanta el servidor:

```bash
uvicorn app.main:app --reload --port 8000
```

Verifica que responde: http://localhost:8000/api/health

Documentación interactiva (Swagger) generada automáticamente:
http://localhost:8000/docs

### 2. Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173

El archivo `frontend/.env` ya apunta a `http://localhost:8000/api` por
defecto — no necesitas tocarlo salvo que cambies el puerto del backend.

## Estructura del proyecto

```
osint-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # osint.py (búsqueda/historial), reports.py (export)
│   │   ├── core/
│   │   │   ├── config.py     # Configuración desde .env
│   │   │   └── i18n.py       # Mensajes traducibles (es/en)
│   │   ├── services/         # Un archivo por fuente OSINT
│   │   ├── models/scan.py    # Modelo de historial (SQLite)
│   │   ├── utils/            # db.py, report_generator.py
│   │   └── main.py           # App FastAPI
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/       # Dashboard, SearchBar, ResultsTable, TechBadge, RelationshipGraph
│   │   ├── pages/             # Home, History
│   │   ├── services/api.js   # Cliente HTTP al backend
│   │   ├── hooks/useOSINT.js
│   │   ├── context/LanguageContext.jsx  # Estado global de idioma (ES/EN)
│   │   ├── i18n/translations.js         # Diccionario de textos
│   │   └── App.jsx            # Incluye el selector de idioma
│   └── package.json
└── README.md
```

## Uso

1. Elige tu idioma (ES/EN) en la esquina superior derecha.
2. Escribe un dominio, IP, email o username en la barra de búsqueda.
3. El dashboard detecta automáticamente el tipo de consulta y llama a las
   fuentes correspondientes en paralelo.
4. Cada búsqueda queda guardada en el historial (pestaña "Historial"/"History").
5. Puedes exportar cualquier resultado a PDF o JSON desde el dashboard o
   desde el historial.

## Endpoints del API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/health` | Estado del servicio |
| GET | `/api/osint/sources` | Qué fuentes tienen API key configurada |
| POST | `/api/osint/search` | `{"query": "...", "lang": "es"\|"en"}` → búsqueda unificada |
| GET | `/api/osint/history?limit=20` | Historial de búsquedas |
| GET | `/api/reports/{id}/pdf` | Descarga reporte en PDF |
| GET | `/api/reports/{id}/json` | Descarga reporte en JSON |

## Siguientes pasos sugeridos

- Agregar tus keys de HaveIBeenPwned y SecurityTrails cuando las tengas
  (no requiere tocar código, solo `.env`)
- Reemplazar el grafo SVG simple de `RelationshipGraph.jsx` por D3.js o
  Vis.js si necesitas relaciones más complejas (múltiples entidades, no
  solo consulta → fuente)
- Si más adelante quieres desplegar en un servidor, se puede volver a
  añadir Docker/Docker Compose y Postgres/Redis como en el diseño original
