# ETL Airbnb México

##  Descripción del Proyecto

Este proyecto implementa un proceso **ETL (Extract, Transform, Load)** completo para el análisis de datos de Airbnb en México. El sistema extrae información de propiedades, reseñas y disponibilidad desde MongoDB, realiza transformaciones y limpieza de datos, y finalmente carga la información normalizada en SQL Server para su análisis.

### Objetivo

Desarrollar un pipeline ETL robusto que permita:
- **Extraer** datos crudos de Airbnb almacenados en MongoDB
- **Transformar** y normalizar los datos eliminando inconsistencias y duplicados
- **Cargar** los datos limpios en SQL Server en un esquema relacional optimizado
- **Registrar** todo el proceso mediante logs detallados para auditoría y debugging

###  Estructura de Datos

El proyecto procesa y genera las siguientes tablas:

| Tabla | Descripción | Registros Aprox. |
|-------|-------------|------------------|
| `listings` | Propiedades disponibles en Airbnb | 15,000+ |
| `host` | Información de anfitriones | 12,000+ |
| `verification` | Métodos de verificación de hosts | 45,000+ |
| `amenities` | Catálogo de amenidades | 150+ |
| `amenities_listings` | Relación amenidades-propiedades | 240,000+ |
| `reviews` | Reseñas de usuarios | 350,000+ |
| `reviewer` | Información de reviewers | 150,000+ |
| `calendar` | Disponibilidad de propiedades | 5,000,000+ |

---

##  Instrucciones de Instalación

###  Requisitos Previos

- **Python 3.8+**
- **MongoDB Community Server** (corriendo en `localhost:27017`)
- **SQL Server 2019+** (Express funciona)
- **ODBC Driver 17 for SQL Server**

### 1️ Clonar o Descargar el Proyecto

```bash
git clone https://github.com/tu-usuario/etl-airbnb-mexico.git
cd etl-airbnb-mexico
```

### 2️ Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️ Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- `pandas>=2.0.0` - Manipulación de datos
- `numpy>=1.24.0` - Operaciones numéricas
- `pymongo>=4.6.0` - Conexión a MongoDB
- `pyodbc>=5.0.0` - Conexión a SQL Server

### 4️ Crear Carpeta de Logs

```bash
# Windows
mkdir logs

# Linux/macOS
mkdir -p logs
```

### 5️ Configurar Conexiones

#### MongoDB (archivo `extraccion.py`)
Si tu MongoDB está en otro servidor o puerto, edita la línea 22:
```python
conexion = pymongo.MongoClient("mongodb://TU_HOST:TU_PUERTO/")
```

#### SQL Server (archivo `carga.py`)
Edita las líneas 23-28 con tus credenciales:
```python
conexion = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=TU_SERVIDOR;"          # ej: localhost o DESKTOP-XXX\SQLEXPRESS
    "DATABASE=AirbnbMexico;"
    "UID=TU_USUARIO;"              # ej: sa o tu usuario SQL
    "PWD=TU_CONTRASEÑA;"
)
```
### 6 Ejecutar el ETL

```bash
python main.py
```

---

## 👥 Integrantes del Grupo

| Nombre | Rol | Responsabilidades |
|--------|-----|-------------------|
| **[Julian Andres Ramirez Bedoya]** | Desarrollador ETL | Implementación de extracción (MongoDB), transformación y carga (SQL Server) |
| **[Maria Jose Gallego Escudero]** | QA / Documentación | Testing, documentación y README |
| **[Juan Jose rUA dAVID]** | Desarrollador ETL | Exploracion Etl , clase Logs, transformación  y integración |


##  Ejemplo de Ejecución del ETL

### Ejecución Completa

```bash
(venv) C:\proyecto> python main.py

================================================================================
LOG DE EJECUCIÓN - EJECUCION
Fecha de inicio: 2025-10-25 09:53:33
================================================================================

[2025-10-25 09:53:33] [INFO] ==================================================
[2025-10-25 09:53:33] [INFO] INICIO DEL PROCESO DE EXTRACCIÓN
[2025-10-25 09:53:33] [INFO] ==================================================
[2025-10-25 09:53:33] [INFO] Intentando conectar a MongoDB (localhost:27017)...
[2025-10-25 09:53:33] [INFO] ✅ Conexión exitosa a MongoDB
[2025-10-25 09:53:33] [INFO] Extrayendo colecciones de la base de datos AirbnMexico...
--------------------------------------------------------------------------------
[2025-10-25 09:53:33] [INFO] Consultando colección: Listings
[2025-10-25 09:53:33] [INFO] Ejecutando consulta en Listings...
[2025-10-25 09:53:34] [INFO] Campo '_id' eliminado del DataFrame
[2025-10-25 09:53:34] [INFO] ✅ Consulta exitosa de Listings
[2025-10-25 09:53:34] [INFO]    - Filas: 26,401
[2025-10-25 09:53:34] [INFO]    - Columnas: 79
[2025-10-25 09:53:34] [INFO]    - Memoria utilizada: 88.34 MB
[2025-10-25 09:53:34] [INFO]    - Columnas: ['id', 'listing_url', 'scrape_id', 'last_scraped', 'source', 'name', 'description', 'neighborhood_overview', 'picture_url', 'host_id', 'host_url', 'host_name', 'host_since', 'host_location', 'host_about', 'host_response_time', 'host_response_rate', 'host_acceptance_rate', 'host_is_superhost', 'host_thumbnail_url', 'host_picture_url', 'host_neighbourhood', 'host_listings_count', 'host_total_listings_count', 'host_verifications', 'host_has_profile_pic', 'host_identity_verified', 'neighbourhood', 'neighbourhood_cleansed', 'neighbourhood_group_cleansed', 'latitude', 'longitude', 'property_type', 'room_type', 'accommodates', 'bathrooms', 'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'price', 'minimum_nights', 'maximum_nights', 'minimum_minimum_nights', 'maximum_minimum_nights', 'minimum_maximum_nights', 'maximum_maximum_nights', 'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm', 'calendar_updated', 'has_availability', 'availability_30', 'availability_60', 'availability_90', 'availability_365', 'calendar_last_scraped', 'number_of_reviews', 'number_of_reviews_ltm', 'number_of_reviews_l30d', 'availability_eoy', 'number_of_reviews_ly', 'estimated_occupancy_l365d', 'estimated_revenue_l365d', 'first_review', 'last_review', 'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication', 'review_scores_location', 'review_scores_value', 'license', 'instant_bookable', 'calculated_host_listings_count', 'calculated_host_listings_count_entire_homes', 'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms', 'reviews_per_month']
--------------------------------------------------------------------------------
[2025-10-25 09:53:34] [INFO] Consultando colección: Reviews
[2025-10-25 09:53:34] [INFO] Ejecutando consulta en Reviews...
[2025-10-25 09:53:54] [INFO] Campo '_id' eliminado del DataFrame
[2025-10-25 09:53:55] [INFO] ✅ Consulta exitosa de Reviews
[2025-10-25 09:53:55] [INFO]    - Filas: 1,388,226
[2025-10-25 09:53:55] [INFO]    - Columnas: 6
[2025-10-25 09:53:55] [INFO]    - Memoria utilizada: 512.60 MB
[2025-10-25 09:53:55] [INFO]    - Columnas: ['listing_id', 'id', 'date', 'reviewer_id', 'reviewer_name', 'comments']
--------------------------------------------------------------------------------
[2025-10-25 09:53:55] [INFO] Consultando colección: Calendar
[2025-10-25 09:53:55] [INFO] Ejecutando consulta en Calendar...
[2025-10-25 10:01:45] [INFO] Campo '_id' eliminado del DataFrame
[2025-10-25 10:01:47] [INFO] ✅ Consulta exitosa de Calendar
[2025-10-25 10:01:47] [INFO]    - Filas: 9,636,365
[2025-10-25 10:01:47] [INFO]    - Columnas: 7
[2025-10-25 10:01:47] [INFO]    - Memoria utilizada: 1203.88 MB
[2025-10-25 10:01:47] [INFO]    - Columnas: ['listing_id', 'date', 'available', 'price', 'adjusted_price', 'minimum_nights', 'maximum_nights']
--------------------------------------------------------------------------------
[2025-10-25 10:01:47] [INFO] Validando datos extraídos...
--------------------------------------------------------------------------------
[2025-10-25 10:01:47] [INFO] RESUMEN DE EXTRACCIÓN:
[2025-10-25 10:01:47] [INFO]   - Listings: 26,401 registros
[2025-10-25 10:01:47] [INFO]   - Reviews: 1,388,226 registros
[2025-10-25 10:01:47] [INFO]   - Calendar: 9,636,365 registros
[2025-10-25 10:01:49] [INFO]   - Memoria total: 1804.82 MB
[2025-10-25 10:01:49] [INFO] Conexión a MongoDB cerrada
[2025-10-25 10:01:49] [INFO] ==================================================
[2025-10-25 10:01:49] [INFO] PROCESO DE EXTRACCIÓN COMPLETADO EXITOSAMENTE
[2025-10-25 10:01:49] [INFO] ==================================================
### Archivos de Log Generados

Después de la ejecución, encontrarás los siguientes logs en la carpeta `logs/`:

```
logs/
├──log_ejecucion_20251025_1027.txt
```
## 📊 Arquitectura del Sistema

```
┌─────────────────┐
│    MongoDB      │  ← Base de datos origen (NoSQL)
│  AirbnMexico    │
└────────┬────────┘
         │
         │ extraccion.py
         ▼
┌─────────────────┐
│   DataFrames    │  ← Datos en memoria (Pandas)
│   Crudos        │
└────────┬────────┘
         │
         │ transformacion.py
         ▼
┌─────────────────┐
│   DataFrames    │  ← Datos limpios y normalizados
│  Transformados  │
└────────┬────────┘
         │
         │ carga.py
         ▼
┌─────────────────┐
│  SQL Server     │  ← Base de datos destino (SQL)
│  AirbnbMexico   │
└─────────────────┘

         ║
         ║ logs.py (registro en todas las fases)
         ▼
┌─────────────────┐
│   logs/*.txt    │  ← Archivos de auditoría
└─────────────────┘
```

---

##  Estructura del Proyecto

```
etl-airbnb-mexico/
│
├── logs/                          # Carpeta para archivos de log
│   ├── log_ejecucion_20251025_1027.txt
├── Notebooks/                     # Carpeta para notebook
    ├── expliracion_airbnb.ipynb   # Notebook de explicación
│
├── logs.py                        # Clase para registro de logs
├── carga.py                       # Módulo de carga (SQL Server)
├── extraccion.py                  # Módulo de extracción (MongoDB)
├── main.py                        # Script principal orquestador
├── transformacion.py              # Módulo de transformación

│
├── requirements.txt               # Dependencias del proyecto
├── README.md                      # Este archivo
```

---

## 🔧 Características Técnicas

### Sistema de Logs
- ✅ Archivo por ejecución con timestamp único
- ✅ Tres niveles: INFO, WARNING, ERROR
- ✅ Registro detallado de cada operación
- ✅ Auditoría completa del proceso

### Extracción
- ✅ Conexión a MongoDB con validación
- ✅ Verificación de colecciones y documentos
- ✅ Manejo de errores de conexión
- ✅ Estadísticas de uso de memoria

### Transformación
- ✅ Normalización de datos (8 tablas relacionales)
- ✅ Limpieza de valores nulos e inconsistencias
- ✅ Eliminación de duplicados
- ✅ Validación de integridad referencial
- ✅ Estandarización de formatos de fecha
- ✅ Normalización de textos (amenidades)

### Carga
- ✅ Creación automática de tablas
- ✅ Mapeo de tipos de datos pandas → SQL
- ✅ Carga en orden (respetando claves foráneas)
- ✅ Manejo de transacciones y rollback
- ✅ Validación de inserción

---

##  Solución de Problemas

### Error: "No module named 'pandas'"
```bash
pip install -r requirements.txt
```

### Error: "MongoDB connection refused"
Verificar que MongoDB esté corriendo:
```bash
# Windows
mongod

# Linux
sudo systemctl start mongod
```

### Error: "SQL Server connection failed"
- Verificar que SQL Server esté corriendo
- Verificar credenciales en `carga.py`
- Verificar que SQL Server Authentication esté habilitado

### Error: "FileNotFoundError: logs"
```bash
mkdir logs
```

---

##  Documentación Adicional

- **REQUISITOS_INSTALACION.md**: Guía detallada de instalación y configuración
- **Logs**: Todos los logs se guardan en `logs/` con timestamp
- **Comentarios en código**: Cada función está documentada

---

##  Métricas del Proyecto

- **Líneas de código**: ~1,500
- **Tablas procesadas**: 8
- **Registros procesados**: ~6.5 millones
- **Tiempo promedio de ejecución**: 10-15 minutos
- **Reducción de datos**: ~17% (limpieza de inconsistencias)

---

## 📄 Licencia

Este proyecto fue desarrollado como parte del curso [Inteligencia de Negocio] en [Intituto Tecnologico Metropolitano].

---

## ✅ Checklist de Ejecución

Antes de ejecutar el ETL, asegúrate de:

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] MongoDB corriendo con datos cargados
- [ ] SQL Server corriendo
- [ ] Base de datos `AirbnbMexico` creada en SQL Server
- [ ] Credenciales configuradas en `carga.py`
- [ ] Carpeta `logs/` creada

✅ **¡Listo para ejecutar!** → `python main.py`
