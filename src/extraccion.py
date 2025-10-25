import pymongo
import pandas as pd
from logs import Logs

__all__ = ['extraer_datos']

def _conectar_mongo(log: Logs):
    """
    Establece conexión con MongoDB.
    
    Args:
        log: Instancia de la clase Logs para registro
        
    Returns:
        pymongo.MongoClient: Objeto de conexión a MongoDB
        
    Raises:
        Exception: Si hay error en la conexión
    """
    try:
        log.info("Intentando conectar a MongoDB (localhost:27017)...")
        conexion = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # Verificar que la conexión es válida
        conexion.server_info()
        
        log.info("✅ Conexión exitosa a MongoDB")
        return conexion
        
    except pymongo.errors.ServerSelectionTimeoutError as e:
        log.error(f"Timeout al conectar con MongoDB: {e}")
        raise Exception(f"❌ Error de conexión: MongoDB no está disponible en localhost:27017")
    except pymongo.errors.ConnectionFailure as e:
        log.error(f"Fallo en la conexión a MongoDB: {e}")
        raise Exception(f"❌ Error de conexión: {e}")
    except Exception as e:
        log.error(f"Error inesperado al conectar con MongoDB: {e}")
        raise Exception(f"❌ Error de conexión: {e}")


def _consulta_mongo(conexion, coleccion: str, log: Logs):
    """
    Realiza consulta a una colección de MongoDB y retorna un DataFrame.
    
    Args:
        conexion: Objeto de conexión a MongoDB
        coleccion: Nombre de la colección a consultar
        log: Instancia de la clase Logs para registro
        
    Returns:
        pd.DataFrame: Datos de la colección
        
    Raises:
        Exception: Si hay error en la consulta
    """
    try:
        log.separator()
        log.info(f"Consultando colección: {coleccion}")
        
        db = conexion["AirbnMexico"]
        collection = db[coleccion]
        
        # Verificar que la colección existe
        if coleccion not in db.list_collection_names():
            log.warning(f"La colección '{coleccion}' no existe en la base de datos")
            return pd.DataFrame()
        
        # Realizar consulta
        log.info(f"Ejecutando consulta en {coleccion}...")
        datos = collection.find()
        df = pd.DataFrame(list(datos))
        
        if df.empty:
            log.warning(f"La colección '{coleccion}' está vacía")
            return df
        
        # Eliminar campo _id de MongoDB
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])
            log.info("Campo '_id' eliminado del DataFrame")
        
        # Información del DataFrame
        memoria_mb = df.memory_usage(deep=True).sum() / 1024**2
        
        log.info(f"✅ Consulta exitosa de {coleccion}")
        log.info(f"   - Filas: {df.shape[0]:,}")
        log.info(f"   - Columnas: {df.shape[1]}")
        log.info(f"   - Memoria utilizada: {memoria_mb:.2f} MB")
        log.info(f"   - Columnas: {list(df.columns)}")
        
        return df
        
    except pymongo.errors.PyMongoError as e:
        log.error(f"Error de MongoDB al consultar '{coleccion}': {e}")
        raise Exception(f"❌ Error de consulta en '{coleccion}': {e}")
    except Exception as e:
        log.error(f"Error inesperado al consultar '{coleccion}': {e}")
        raise Exception(f"❌ Error de consulta en '{coleccion}': {e}")


def extraer_datos(log: Logs):
    """
    Función principal para extraer datos de MongoDB.
    Extrae las colecciones: listings, reviews y calendar.
    
    Returns:
        tuple: (df_listings, df_reviews, df_calendar)
    """
    conexion = None
    
    try:
        log.info("=" * 50)
        log.info("INICIO DEL PROCESO DE EXTRACCIÓN")
        log.info("=" * 50)
        
        # Conectar a MongoDB
        conexion = _conectar_mongo(log)
        
        # Extraer colecciones
        log.info("Extrayendo colecciones de la base de datos AirbnMexico...")
        
        df_listings = _consulta_mongo(conexion, "Listings", log)
        df_reviews = _consulta_mongo(conexion, "Reviews", log)
        df_calendar = _consulta_mongo(conexion, "Calendar", log)
        
        # Validar que se extrajeron datos
        log.separator()
        log.info("Validando datos extraídos...")
        
        if df_listings.empty:
            log.error("La tabla 'listings' está vacía")
            raise Exception("No se pueden procesar datos sin listings")
        
        if df_reviews.empty:
            log.warning("La tabla 'reviews' está vacía")
        
        if df_calendar.empty:
            log.warning("La tabla 'calendar' está vacía")
        
        # Resumen final
        log.separator()
        log.info("RESUMEN DE EXTRACCIÓN:")
        log.info(f"  - Listings: {df_listings.shape[0]:,} registros")
        log.info(f"  - Reviews: {df_reviews.shape[0]:,} registros")
        log.info(f"  - Calendar: {df_calendar.shape[0]:,} registros")
        
        total_memoria = (
            df_listings.memory_usage(deep=True).sum() +
            df_reviews.memory_usage(deep=True).sum() +
            df_calendar.memory_usage(deep=True).sum()
        ) / 1024**2
        
        log.info(f"  - Memoria total: {total_memoria:.2f} MB")
        
        return df_listings, df_reviews, df_calendar
        
    except Exception as e:
        log.error(f"Error crítico en extraer_datos: {str(e)}")
        raise
    
    finally:
        # Cerrar conexión a MongoDB
        if conexion is not None:
            conexion.close()
            log.info("Conexión a MongoDB cerrada")

        log.info("=" * 50)
        log.info("PROCESO DE EXTRACCIÓN COMPLETADO EXITOSAMENTE")
        log.info("=" * 50)