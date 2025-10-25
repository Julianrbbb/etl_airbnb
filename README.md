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

### Contribuciones Específicas

- **Extracción (`extraccion.py`)**: [Nombre 2]
- **Transformación (`transformacion.py`)**: [Nombre 3]
- **Carga (`carga.py`)**: [Nombre 4]
- **Sistema de Logs (`logs.py`)**: [Nombre 2]
- **Integración (`main.py`)**: [Nombre 1]
- **Documentación y Testing**: [Nombre 5]

---

##  Ejemplo de Ejecución del ETL

### Ejecución Completa

```bash
(venv) C:\proyecto> python main.py

================================================================================
PROCESO ETL - AIRBNB MÉXICO
================================================================================
Inicio: 2025-10-24 14:30:45

================================================================================
FASE 1: EXTRACCIÓN DE DATOS DESDE MONGODB
================================================================================

Extracción completada:
   - Listings: 18,431 registros
   - Reviews: 368,325 registros
   - Calendar: 6,727,315 registros

================================================================================
FASE 2: TRANSFORMACIÓN Y NORMALIZACIÓN DE DATOS
================================================================================

 Transformación completada:
   - Listings: 15,234 registros
   - Host: 12,450 registros
   - Verification: 45,823 registros
   - Amenities: 156 registros
   - Amenities-Listings: 245,892 registros
   - Reviews: 352,108 registros
   - Reviewer: 168,234 registros
   - Calendar: 5,562,261 registros

================================================================================
FASE 3: CARGA DE DATOS A SQL SERVER
================================================================================

 Carga completada

================================================================================
 PROCESO ETL COMPLETADO EXITOSAMENTE
================================================================================
Fin: 2025-10-24 14:45:22

Revisa los logs en la carpeta 'logs/' para más detalles
================================================================================
```

### Archivos de Log Generados

Después de la ejecución, encontrarás los siguientes logs en la carpeta `logs/`:

```
logs/
├── log_extraccion_20251024_1430.txt
├── log_transformacion_20251024_1435.txt
└── log_carga_20251024_1442.txt
```

### Ejemplo de Contenido de Log

**log_transformacion_20251024_1435.txt:**
```
================================================================================
LOG DE EJECUCIÓN - TRANSFORMACION
Fecha de inicio: 2025-10-24 14:35:12
================================================================================

[2025-10-24 14:35:12] [INFO] ==============================================================
[2025-10-24 14:35:12] [INFO] INICIO DEL PROCESO DE TRANSFORMACIÓN
[2025-10-24 14:35:12] [INFO] ==============================================================
--------------------------------------------------------------------------------
[2025-10-24 14:35:12] [INFO] 4.1. Abstracción de df_host
[2025-10-24 14:35:12] [INFO] Se abstrae el df_host del df_listings
[2025-10-24 14:35:13] [INFO] ✅ df_host - Filas: 12,856, Columnas: 18
--------------------------------------------------------------------------------
[2025-10-24 14:35:13] [INFO] 4.2. Eliminación de campos no necesarios en df_host
[2025-10-24 14:35:13] [INFO] ✅ df_host - Filas: 12,856, Columnas: 11
--------------------------------------------------------------------------------
[2025-10-24 14:35:13] [INFO] 4.3. Limpieza del df_host
[2025-10-24 14:35:13] [INFO] Eliminación de host con nombre, verificación y locación null
[2025-10-24 14:35:14] [INFO] Eliminados 406 hosts sin información válida
[2025-10-24 14:35:14] [INFO] Transformando campos de fecha a formato estándar
[2025-10-24 14:35:14] [INFO] ✅ df_host - Filas: 12,450, Columnas: 11
...
```

### Ejecución por Fases (Opcional)

Si deseas ejecutar solo una fase específica:

**Solo Extracción:**
```python
from extraccion import extraer_datos
df_listings, df_reviews, df_calendar = extraer_datos()
```

**Solo Transformación:**
```python
from transformacion import transformacion_df
result = transformacion_df(df_listings, df_reviews, df_calendar)
```

**Solo Carga:**
```python
from carga import cargar_datos
cargar_datos(df_listings, df_reviews, df_calendar, df_host, ...)
```

---

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
│   ├── log_extraccion_*.txt
│   ├── log_transformacion_*.txt
│   └── log_carga_*.txt
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
net start MongoDB

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
- [ ] Verificación ejecutada (`python verificar_requisitos.py`)

✅ **¡Listo para ejecutar!** → `python main.py`
