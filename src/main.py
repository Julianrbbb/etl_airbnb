from extraccion import *
from transformacion import *
from carga import *
from logs import Logs

def main():
    try:

        log = Logs(script_name="ejecucion")
        log.separator()
        log.separator()
        df_listings, df_reviews, df_calendar = extraer_datos(log)
        log.separator()
        log.separator()
        df_listings, df_reviews, df_calendar, df_host, df_verification, df_amenities_listings, df_amenities, df_reviewer = transformacion_df(df_listings, df_reviews, df_calendar, log)
        log.separator()
        log.separator()
        cargar_datos(df_listings, df_reviews, df_calendar, df_host, df_verification, df_amenities_listings, df_amenities, df_reviewer, log)
        log.separator()
        log.separator()

    finally:
        log.close()

if __name__ == "__main__":
    main()