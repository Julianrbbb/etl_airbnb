from extraccion import conectar_mongo, consulta_mongo
from transformacion import *

def main():
    try:
        print("=== Conexión a MongoDB desde Python ===\n")

        # 1. Conectar a MongoDB
        conexion = conectar_mongo()

        # 2. Consultar datos
        df_listings = consulta_mongo(conexion, "Listings")
        #df_reviews = consulta_mongo(conexion, "Reviews")
        #df_calendar = consulta_mongo(conexion, "Calendar")

        # 4. Transformacion datos
        transformacion_df(df_listings)

        # 3. Cerrar conexión
        conexion.close()
        print("\n🔒 Conexión cerrada")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()