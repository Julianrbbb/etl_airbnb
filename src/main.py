from extraccion import conectar_mongo, consulta_mongo
from transformacion import *

def main():
    try:
        print("=== App ETL Airbnb")

        print("\n1. Conectar a MongoDB")
        conexion = conectar_mongo()

        print("\n2. Consultar datos")
        df_listings_o = consulta_mongo(conexion, "Listings")
        df_reviews_o = consulta_mongo(conexion, "Reviews")
        df_calendar_o = consulta_mongo(conexion, "Calendar")

        print("\n4. Transformacion datos")
        df_listings, df_reviews, df_calendar, df_host, df_verification, df_reviewer = transformacion_df(df_listings_o, df_reviews_o, df_calendar_o)

        # 3. Cerrar conexión
        conexion.close()
        print("\n🔒 Conexión cerrada")

    except Exception as e:
        conexion.close()
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()