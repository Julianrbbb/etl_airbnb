from extraccion import conectar_mongo, consulta_mongo
from transformacion import *
from carga import *

def main():
    try:
        print("=== App ETL Airbnb")

        print("\n1. Conectar a MongoDB")
        conexionMONGO = conectar_mongo()

        print("\n2. Consultar datos")
        df_listings_o = consulta_mongo(conexionMONGO, "Listings")
        df_reviews_o = consulta_mongo(conexionMONGO, "Reviews")
        df_calendar_o = consulta_mongo(conexionMONGO, "Calendar")

        print("\n4. Transformacion datos")
        df_listings, df_reviews, df_calendar, df_host, df_verification, df_amenities_listings, df_amenities, df_reviewer = transformacion_df(df_listings_o, df_reviews_o, df_calendar_o)

        print("\n5. Cargar datos")
        conexionSQL = conectar_sql()
        cargar_data_frame(conexionSQL, df_listings, "listings")
        cargar_data_frame(conexionSQL, df_host, "host")
        cargar_data_frame(conexionSQL, df_verification, "verification")
        cargar_data_frame(conexionSQL, df_amenities_listings, "amenities_listings")
        cargar_data_frame(conexionSQL, df_amenities, "amenities")
        cargar_data_frame(conexionSQL, df_reviews, "reviews")
        cargar_data_frame(conexionSQL, df_reviewer, "reviewer")
        cargar_data_frame(conexionSQL, df_calendar, "calendar")

        # 3. Cerrar conexión
        conexionMONGO.close()
        conexionSQL.close()
        print("\n🔒 Conexiónes cerradas")

    except Exception as e:
        conexionMONGO.close()
        conexionSQL.close()
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()