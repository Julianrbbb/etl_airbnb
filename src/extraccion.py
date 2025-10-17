import pymongo
import pandas as pd

def conectar_mongo():
    try:
        conexion = pymongo.MongoClient("mongodb://localhost:27017/")
        print("✅ Conexión exitosa a MongoDB")
        return conexion
    except pymongo.Error as e:
        print(f"❌ Error de conexión: {e}")
        return None

def consulta_mongo(conexion, coleccion):
    try:
        db = conexion["AirbnMexico"]
        collection = db[coleccion]
        datos = collection.find()
        df = pd.DataFrame(list(datos))

        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        print(f"\n✅ Consulta exitosa de {coleccion}")
        print(f"   - Filas: {df.shape[0]}")
        print(f"   - Columnas: {df.shape[1]}")
        print(f"   - Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"   - Primeros 5 registros: \n{df.head()}")
        return df

    except pymongo.Error as e:
        print(f"❌ Error de consulta: {e}")
        return None

def main():
    print("=== Conexión a MongoDB desde Python ===\n")
    # 1. Conectar a MongoDB
    conexion = conectar_mongo()
    
    if conexion:
        # Cargar datos de las colecciones
        df_listings = consulta_mongo(conexion, "Listings")
        df_reviews = consulta_mongo(conexion, "Reviews")
        df_calendar = consulta_mongo(conexion, "Calendar")
        
        # Cerrar conexión
        conexion.close()
        print("\n🔒 Conexión cerrada")

if __name__ == "__main__":
    main()