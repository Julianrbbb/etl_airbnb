import pandas as pd
import pyodbc
import numpy as np
from logs import Logs

__all__ = ['cargar_datos']

def _conectar_sql(log: Logs):
    try:
        log.info("Intentando conectar a SQL Server...")
        log.info("Servidor: DESKTOP-Q68QGU3\\JUSERVER")
        log.info("Base de datos: AirbnbMexico")
        
        conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-Q68QGU3\\JUSERVER;"
            "DATABASE=AirbnbMexico;"
            "UID=Universidad;"
            "PWD=itm2025*;"
        )
        
        log.info("✅ Conexión exitosa a SQL Server")
        return conexion
        
    except pyodbc.Error as e:
        log.error(f"Error al conectar con SQL Server: {e}")
        raise Exception(f"❌ Error de conexión: {e}")
    except Exception as e:
        log.error(f"Error inesperado al conectar: {e}")
        raise Exception(f"❌ Error de conexión: {e}")


def _cargar_data_frame(conexion, df: pd.DataFrame, table_name: str, log: Logs, i: int, totalTablas: int):
    """
    Carga un DataFrame en una tabla de SQL Server.
    
    Args:
        conexion: Objeto de conexión a SQL Server
        df: DataFrame a cargar
        table_name: Nombre de la tabla destino
        log: Instancia de la clase Logs para registro
    """
    try:
        log.separator()
        log.info(f"[{i}/{totalTablas}] Cargando tabla: {table_name}")
        log.info(f"Iniciando carga de tabla: {table_name}")
        log.info(f"Registros a cargar: {len(df):,}")
        log.info(f"Columnas: {df.shape[1]}")
        
        _crear_tabla(conexion, df, table_name, log)
        _insertar_data(conexion, df, table_name, log)
        
        log.info(f"✅ Tabla {table_name} cargada exitosamente")
        return True

    except Exception:
        return False


def _crear_tabla(conexion, df: pd.DataFrame, table_name: str, log: Logs):
    """
    Crea una tabla en SQL Server basada en el DataFrame.
    Si la tabla existe, la limpia.
    
    Args:
        conexion: Objeto de conexión a SQL Server
        df: DataFrame para definir estructura
        table_name: Nombre de la tabla
        log: Instancia de la clase Logs
    """
    try:
        cursor = conexion.cursor()
        
        # Verificar si la tabla existe
        log.info(f"Verificando existencia de tabla [{table_name}]...")
        
        check_query = f"""
            IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}')
                SELECT 1 AS existe
            ELSE
                SELECT 0 AS existe
        """
        cursor.execute(check_query)
        existe = cursor.fetchone()[0]
        
        if existe:
            log.info(f"Tabla [{table_name}] ya existe. Limpiando datos...")
            cursor.execute(f"TRUNCATE TABLE [{table_name}];")
            conexion.commit()
            log.info(f"✅ Tabla [{table_name}] limpiada correctamente")
            return
        
        # Crear la tabla si no existe
        log.info(f"Tabla [{table_name}] no existe. Creando estructura...")
        
        dtype_map_sqlserver = {
            'object': 'NVARCHAR(MAX)',
            'string': 'NVARCHAR(MAX)',
            'int64': 'BIGINT',
            'int32': 'INT',
            'float64': 'DECIMAL(20,7)',
            'float32': 'DECIMAL(20,7)',
            'bool': 'BIT',
            'boolean': 'BIT',
            'datetime64[ns]': 'DATETIME',
            'datetime64': 'DATETIME'
        }
        
        columns = []
        for col, dtype in df.dtypes.items():
            sql_type = dtype_map_sqlserver.get(str(dtype), 'NVARCHAR(MAX)')
            columns.append(f'[{col}] {sql_type}')
            log.info(f"  - Columna [{col}]: {sql_type}")
        
        columns_sql = ",\n  ".join(columns)
        query = f'CREATE TABLE [{table_name}] (\n  {columns_sql}\n);'
        
        cursor.execute(query)
        conexion.commit()
        
        log.info(f"✅ Tabla [{table_name}] creada correctamente en SQL Server")
        log.info(f"✅ Total de columnas: {len(columns)}")
        
    except pyodbc.Error as e:
        log.error(f"Error de SQL al crear tabla [{table_name}]: {e}")
        raise
    except Exception as e:
        log.error(f"Error inesperado al crear tabla [{table_name}]: {e}")
        raise


def _insertar_data(conexion, df: pd.DataFrame, table_name: str, log: Logs):
    """
    Inserta los datos del DataFrame en la tabla de SQL Server.
    
    Args:
        conexion: Objeto de conexión a SQL Server
        df: DataFrame con los datos a insertar
        table_name: Nombre de la tabla destino
        log: Instancia de la clase Logs
    """
    try:
        cursor = conexion.cursor()
        
        log.info(f"Preparando datos para inserción en [{table_name}]...")
        
        # Convertir valores de pandas/numpy a tipos nativos de Python
        df = df.apply(lambda col: col.map(_to_python_value))
        
        cols = ", ".join(f"[{c}]" for c in df.columns)
        placeholders = ", ".join("?" for _ in df.columns)
        sql = f"INSERT INTO [{table_name}] ({cols}) VALUES ({placeholders})"
        
        # Convertir DataFrame a lista de tuplas
        log.info(f"Convirtiendo {len(df):,} filas a formato SQL...")
        data = [tuple(_to_python_value(x) for x in row) for row in df.to_numpy()]
        #data = [tuple(None if pd.isna(x) else x for x in row) for row in df.to_numpy()]
        
        log.info(f"Insertando datos en [{table_name}]...")
        cursor.executemany(sql, data)
        conexion.commit()
        
        log.info(f"✅ {len(df):,} filas insertadas en [{table_name}] correctamente")
        
    except pyodbc.Error as e:
        log.error(f"Error de SQL al insertar datos en [{table_name}]: {e}")
        conexion.rollback()
        log.warning(f"Se hizo rollback de la transacción")
        raise
    except Exception as e:
        log.error(f"Error inesperado al insertar datos en [{table_name}]: {e}")
        conexion.rollback()
        log.warning(f"Se hizo rollback de la transacción")
        raise


def _to_python_value(x):
  
    if pd.isna(x):
        return None
    if isinstance(x, (np.integer, np.int64, np.int32)):
        return int(x)
    if isinstance(x, (np.floating, np.float64, np.float32)):
        return float(x)
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, (pd.Timestamp,)):
        return x.to_pydatetime()
    return str(x) if not isinstance(x, (int, float, bool)) else x


def cargar_datos(df_listings, df_reviews, df_calendar, df_host, df_verification, 
    df_amenities_listings, df_amenities, df_reviewer, log: Logs):

    conexion = None
    
    try:
        log.info("=" * 50)
        log.info("INICIO DEL PROCESO DE CARGA")
        log.info("=" * 50)
        
        # Conectar a SQL Server
        conexion = _conectar_sql(log)
        
        # Definir orden de carga (tablas padre primero)
        tablas = [
            (df_host, "host"),
            (df_verification, "verification"),
            (df_amenities, "amenities"),
            (df_reviewer, "reviewer"),
            (df_listings, "listings"),
            (df_amenities_listings, "amenities_listings"),
            (df_reviews, "reviews"),
            (df_calendar, "calendar")
        ]
        
        log.separator()
        log.info("Resumen de tablas a cargar:")
        for df, nombre in tablas:
            log.info(f"  - {nombre}: {len(df):,} registros, {df.shape[1]} columnas")
        
        # Cargar cada tabla
        total_registros = 0
        for i, (df, nombre) in enumerate(tablas, 1):
            exitoso = _cargar_data_frame(conexion, df, nombre, log, i, len(tablas))
            if exitoso:
                total_registros += len(df)
        
        # Resumen final
        log.separator()
        log.info("RESUMEN DE CARGA:")
        log.info(f"  - Tablas cargadas: {len(tablas)}")
        log.info(f"  - Total de registros: {total_registros:,}")
        log.info(f"  - Base de datos: AirbnbMexico")
        
    except Exception as e:
        log.error(f"Error crítico en cargar_datos: {str(e)}")
        raise
    
    finally:
        if conexion is not None:
            conexion.close()
            log.info("Conexión a SQL Server cerrada")
    
        log.info("=" * 50)
        log.info("PROCESO DE CARGA COMPLETADO EXITOSAMENTE")
        log.info("=" * 50)