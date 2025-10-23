import pymongo
import pandas as pd

def conectar_mongo():
    try:
        conexion = pymongo.MongoClient("mongodb://localhost:27017/")
        print("✅ Conexión exitosa a MongoDB")
        return conexion
    except pymongo.Error as e:
        raise Exception(f"❌ Error de conexión: {e}")

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
        raise Exception(f"❌ Error de consulta: {e}")