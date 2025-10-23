import pandas as pd
import numpy as np
import ast

__all__ = ['transformacion_df']

def transformacion_df(df_listings: pd.DataFrame, df_reviews: pd.DataFrame, df_calendar: pd.DataFrame):

    df_listings, df_host, df_verification = _transformacion_listings(df_listings)

    return

def _transformacion_listings(df_listings: pd.DataFrame):

    print("\n✅ 1. Abstracion de df_host")
    print("Se abstrae el df_host del df_listings")

    df_host = df_listings[['host_id', 'host_url', 'host_name', 'host_since', 
        'host_location', 'host_about', 'host_response_time', 'host_response_rate',
        'host_acceptance_rate', 'host_is_superhost', 'host_thumbnail_url', 'host_picture_url',
        'host_neighbourhood', 'host_listings_count', 'host_total_listings_count', 'host_verifications',
        'host_has_profile_pic', 'host_identity_verified']].drop_duplicates()
    
    print("\ndf_host")
    print(f"   - Filas: {df_host.shape[0]}")
    print(f"   - Columnas: {df_host.shape[1]}")

    print("\n✅ 2. Eliminacion de campos no necesarios en df_host")
    print("Campos: host_response_time, host_response_rate, host_acceptance_rate, host_thumbnail_url, host_picture_url, host_neighbourhood, host_has_profile_pic")

    df_host = df_host.drop(['host_response_time', 'host_response_rate', 'host_acceptance_rate', 
        'host_thumbnail_url', 'host_picture_url', 'host_neighbourhood', 
        'host_has_profile_pic'], axis=1)

    print("\ndf_host")
    print(f"   - Filas: {df_host.shape[0]}")
    print(f"   - Columnas: {df_host.shape[1]}")

    print("\n✅ 3. Limpieza del df_host")
    print("Eliminacion de host con nombre, verifiacion y locacion null")

    df_host = df_host[~(df_host['host_name'].isnull() | (df_host['host_name'] == ''))]
    df_host = df_host[~(df_host['host_verifications'] == 'None')]
    df_host = df_host[~(df_host['host_location'] == '')]

    print("Se transformara los campos de fecha a un formato estandar.")
    df_host['host_since'] = pd.to_datetime(df_host['host_since'])

    print("\ndf_host")
    print(f"   - Filas: {df_host.shape[0]}")
    print(f"   - Columnas: {df_host.shape[1]}")

    print("\n✅ 4. Abtracion de df_verification")
    print("Se abstrae en una df las formas de verificaciones que tiene cada host y se elimina del df_host")

    #Se transformo el campo host_verifications de string a list
    df_host['host_verifications'] = df_host['host_verifications'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    df_verification = (
        df_host[['host_id', 'host_verifications']]
        .explode('host_verifications')
        .reset_index(drop=True)
    )
    df_verification.insert(0, 'verification_id', df_verification.index + 1)
    df_verification['host_verifications'] = df_verification['host_verifications'].str.strip()
    df_host = df_host.drop(['host_verifications'], axis=1)

    print("\ndf_host")
    print(f"   - Filas: {df_host.shape[0]}")
    print(f"   - Columnas: {df_host.shape[1]}")
    print(f"   - Primeros 5 registros: \n{df_host.head()}")

    print("\ndf_verification")
    print(f"   - Filas: {df_verification.shape[0]}")
    print(f"   - Columnas: {df_verification.shape[1]}")
    print(f"   - Primeros 5 registros: \n{df_verification.head()}")

    print("\n✅ 5. Limpieza de df_listings validando con df_host")
    print("Se eliminaran los campos de df_host y se limpiara todos los listings que no tengan un host valido")

    df_listings = df_listings.drop(['host_url', 'host_name', 'host_since', 
        'host_location', 'host_about', 'host_response_time', 'host_response_rate',
        'host_acceptance_rate', 'host_is_superhost', 'host_thumbnail_url', 'host_picture_url',
        'host_neighbourhood', 'host_listings_count', 'host_total_listings_count', 'host_verifications',
        'host_has_profile_pic', 'host_identity_verified'], axis=1)

    df_listings = df_listings[df_listings['host_id'].isin(df_host['host_id'])]
    print("\ndf_listings")
    print(f"   - Filas: {df_listings.shape[0]}")
    print(f"   - Columnas: {df_listings.shape[1]}")

    print("\n✅ 6. Eliminacion de campos df_listing")
    print("Se eliminaran los campos redundantes o con informacion incompleta o no valiosa para nuestro caso")

    df_listings = df_listings.drop(['scrape_id', 'source', 'picture_url', 'neighbourhood_group_cleansed', 'minimum_minimum_nights', 
        'maximum_minimum_nights', 'minimum_maximum_nights', 'maximum_maximum_nights', 'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm',
        'calendar_updated', 'calendar_last_scraped', 'license', 'instant_bookable', 'calculated_host_listings_count', 
        'calculated_host_listings_count_entire_homes', 'calculated_host_listings_count_private_rooms', 
        'calculated_host_listings_count_shared_rooms', 'bathrooms', 'availability_30','availability_60',
        'availability_90','availability_365', 'availability_eoy', 'number_of_reviews_ltm', 'number_of_reviews_l30d',
        'number_of_reviews_ly', 'reviews_per_month', 'neighbourhood'], axis=1)

    print("\ndf_listings")
    print(f"   - Filas: {df_listings.shape[0]}")
    print(f"   - Columnas: {df_listings.shape[1]}")

    print("\n✅ 7. Limpiza de campos df_listing")

    print("Se eliminaran listings que no cumplan con al menos una review.")
    df_listings = df_listings[~(df_listings['number_of_reviews'] <= 0)]

    print("Se transformara los campos de fecha a un formato estandar.")
    df_listings['last_scraped'] = pd.to_datetime(df_listings['last_scraped'])
    df_listings['first_review'] = pd.to_datetime(df_listings['first_review'])
    df_listings['last_review'] = pd.to_datetime(df_listings['last_review'])

    print("Se eliminaran listings que no cumplan con una review con un año de antiguedad calculada con el campo last_scraped y last_review.")
    df_listings = df_listings[~(df_listings['last_review'] < (df_listings['last_scraped'] - pd.DateOffset(years=1)))]

    print("Transformacion de precio en listing y filtrado de precios no validos")
    df_listings = df_listings[~(df_listings['price'] == '')]
    df_listings['price'] = (
        df_listings['price']
        .replace('[\$,]', '', regex=True)
        .astype(float)
    )

    print("Ajuste de campos bathrooms_text, bedrooms, beds")
    df_listings['beds'] = df_listings['beds'].replace(0, 1)
    df_listings['bedrooms'] = df_listings['bedrooms'].replace(0, 1)
    df_listings['bathrooms_text'] = df_listings['bathrooms_text'].replace('', 1)

    df_listings['bathrooms_text'] = (
        df_listings['bathrooms_text']
        .str.extract(r'(\d+\.?\d*)')
        .astype(float)
    )

    df_listings['bathrooms_text'] = df_listings['bathrooms_text'].fillna(1)
    df_listings['bathrooms_text'] = np.ceil(df_listings['bathrooms_text']).astype(int)

    # Se da formato YYYY-MM-DD
    df_listings['last_scraped'] = df_listings['last_scraped'].dt.strftime('%Y-%m-%d')
    df_listings['first_review'] = df_listings['first_review'].dt.strftime('%Y-%m-%d')
    df_listings['last_review'] = df_listings['last_review'].dt.strftime('%Y-%m-%d')
    df_host['host_since'] = df_host['host_since'].dt.strftime('%Y-%m-%d')

    print("\ndf_listings")
    print(f"   - Filas: {df_listings.shape[0]}")
    print(f"   - Columnas: {df_listings.shape[1]}")
    print(f"   - Primeros 5 registros: \n{df_listings.head()}")

    return (df_listings, df_host, df_verification)