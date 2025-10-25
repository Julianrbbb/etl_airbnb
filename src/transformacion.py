import pandas as pd
import numpy as np
import ast
import unicodedata
from logs import Logs

__all__ = ['transformacion_df']

def transformacion_df(df_listings: pd.DataFrame, 
    df_reviews: pd.DataFrame, 
    df_calendar: pd.DataFrame, 
    log: Logs):
    try:
        log.info("=" * 50)
        log.info("INICIO DEL PROCESO DE TRANSFORMACIÓN")
        log.info("=" * 50)
        
        df_listings, df_host, df_verification, df_amenities_listings, df_amenities = _transformacion_listings(df_listings, log)
        df_reviews, df_reviewer = _transformacion_reviews(df_reviews, df_listings['id'], log)
        df_calendar = _transformacion_calendar(df_calendar, df_listings['id'], log)

        return df_listings, df_reviews, df_calendar, df_host, df_verification, df_amenities_listings, df_amenities, df_reviewer
        
    except Exception as e:
        log.error(f"Error crítico en transformacion_df: {str(e)}")
        raise

    finally:
        log.info("=" * 50)
        log.info("PROCESO DE TRANSFORMACIÓN COMPLETADO EXITOSAMENTE")
        log.info("=" * 50)


def _transformacion_listings(df_listings: pd.DataFrame, log: Logs):
    """Transforma listings y extrae tablas relacionadas."""
    try:
        # 4.1 Abstracción de df_host
        log.separator()
        log.info("4.1. Abstracción de df_host")
        log.info("Se abstrae el df_host del df_listings")
        
        df_host = df_listings[['host_id', 'host_url', 'host_name', 'host_since', 
            'host_location', 'host_about', 'host_response_time', 'host_response_rate',
            'host_acceptance_rate', 'host_is_superhost', 'host_thumbnail_url', 'host_picture_url',
            'host_neighbourhood', 'host_listings_count', 'host_total_listings_count', 'host_verifications',
            'host_has_profile_pic', 'host_identity_verified']].drop_duplicates()
        
        log.info(f"✅ df_host - Filas: {df_host.shape[0]:,}, Columnas: {df_host.shape[1]}")
        
        # 4.2 Eliminación de campos no necesarios
        log.separator()
        log.info("4.2. Eliminación de campos no necesarios en df_host")
        
        campos_eliminar = ['host_response_time', 'host_response_rate', 'host_acceptance_rate', 
            'host_thumbnail_url', 'host_picture_url', 'host_neighbourhood', 'host_has_profile_pic']
        
        df_host = df_host.drop(campos_eliminar, axis=1)
        log.info(f"✅ df_host - Filas: {df_host.shape[0]:,}, Columnas: {df_host.shape[1]}")
        
        # 4.3 Limpieza del df_host
        log.separator()
        log.info("4.3. Limpieza del df_host")
        log.info("Eliminación de host con nombre, verificación y locación null")
        
        filas_antes = df_host.shape[0]
        df_host = df_host[~(df_host['host_name'].isnull() | (df_host['host_name'] == ''))]
        df_host = df_host[~(df_host['host_verifications'] == 'None')]
        df_host = df_host[~(df_host['host_location'] == '')]
        
        log.info(f"Eliminados {filas_antes - df_host.shape[0]:,} hosts sin información válida")
        log.info("Transformando campos de fecha a formato estándar")
        df_host['host_since'] = pd.to_datetime(df_host['host_since'])
        
        log.info(f"✅ df_host - Filas: {df_host.shape[0]:,}, Columnas: {df_host.shape[1]}")
        
        # 4.4 Abstracción de verificaciones
        log.separator()
        log.info("4.4. Abstracción de df_verification")
        log.info("Se abstrae las formas de verificaciones que tiene cada host")
        
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
        
        log.info(f"✅ df_host - Filas: {df_host.shape[0]:,}, Columnas: {df_host.shape[1]}")
        log.info(f"✅ df_verification - Filas: {df_verification.shape[0]:,}, Columnas: {df_verification.shape[1]}")
        
        # 4.5 Limpieza de df_listings
        log.separator()
        log.info("4.5. Limpieza de df_listings validando con df_host")
        
        campos_host = ['host_url', 'host_name', 'host_since', 'host_location', 'host_about', 
            'host_response_time', 'host_response_rate', 'host_acceptance_rate', 'host_is_superhost', 
            'host_thumbnail_url', 'host_picture_url', 'host_neighbourhood', 'host_listings_count', 
            'host_total_listings_count', 'host_verifications', 'host_has_profile_pic', 'host_identity_verified']
        
        df_listings = df_listings.drop(campos_host, axis=1)
        
        filas_antes = df_listings.shape[0]
        df_listings = df_listings[df_listings['host_id'].isin(df_host['host_id'])]
        
        log.info(f"Eliminados {filas_antes - df_listings.shape[0]:,} listings sin host válido")
        log.info(f"✅ df_listings - Filas: {df_listings.shape[0]:,}, Columnas: {df_listings.shape[1]}")
        
        # 4.6 Eliminación de campos redundantes
        log.separator()
        log.info("4.6. Eliminación de campos redundantes de df_listings")
        
        campos_redundantes = ['scrape_id', 'source', 'picture_url', 'neighbourhood_group_cleansed', 
            'minimum_minimum_nights', 'maximum_minimum_nights', 'minimum_maximum_nights', 
            'maximum_maximum_nights', 'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm',
            'calendar_updated', 'calendar_last_scraped', 'license', 'instant_bookable', 
            'calculated_host_listings_count', 'calculated_host_listings_count_entire_homes', 
            'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms', 
            'bathrooms', 'availability_30','availability_60', 'availability_90','availability_365', 
            'availability_eoy', 'number_of_reviews_ltm', 'number_of_reviews_l30d',
            'number_of_reviews_ly', 'reviews_per_month', 'neighbourhood']
        
        df_listings = df_listings.drop(campos_redundantes, axis=1)
        log.info(f"✅ df_listings - Columnas: {df_listings.shape[1]}")
        
        # 4.7 Limpieza de campos
        log.separator()
        log.info("4.7. Limpieza de campos df_listings")
        
        filas_antes = df_listings.shape[0]
        df_listings = df_listings[~(df_listings['number_of_reviews'] <= 0)]
        log.info(f"Eliminados {filas_antes - df_listings.shape[0]:,} listings sin reviews")
        
        log.info("Transformando campos de fecha a formato estándar")
        df_listings['last_scraped'] = pd.to_datetime(df_listings['last_scraped'])
        df_listings['first_review'] = pd.to_datetime(df_listings['first_review'])
        df_listings['last_review'] = pd.to_datetime(df_listings['last_review'])
        
        filas_antes = df_listings.shape[0]
        df_listings = df_listings[~(df_listings['last_review'] < (df_listings['last_scraped'] - pd.DateOffset(years=1)))]
        log.info(f"Eliminados {filas_antes - df_listings.shape[0]:,} listings con reviews antiguas (>1 año)")
        
        log.info("Transformando y validando precios")
        filas_antes = df_listings.shape[0]
        df_listings = df_listings[~(df_listings['price'] == '')]
        df_listings['price'] = df_listings['price'].replace('[\$,]', '', regex=True).astype(float)
        log.info(f"Eliminados {filas_antes - df_listings.shape[0]:,} listings con precios inválidos")
        
        log.info("Ajustando campos bathrooms_text, bedrooms, beds")
        df_listings['beds'] = df_listings['beds'].replace(0, 1)
        df_listings['bedrooms'] = df_listings['bedrooms'].replace(0, 1)
        df_listings['bathrooms_text'] = df_listings['bathrooms_text'].replace('', 1)
        df_listings['bathrooms_text'] = df_listings['bathrooms_text'].str.extract(r'(\d+\.?\d*)').astype(float)
        df_listings['bathrooms_text'] = df_listings['bathrooms_text'].fillna(1)
        df_listings['bathrooms_text'] = np.ceil(df_listings['bathrooms_text']).astype(int)
        
        df_listings['last_scraped'] = df_listings['last_scraped'].dt.strftime('%Y-%m-%d')
        df_listings['first_review'] = df_listings['first_review'].dt.strftime('%Y-%m-%d')
        df_listings['last_review'] = df_listings['last_review'].dt.strftime('%Y-%m-%d')
        df_host['host_since'] = df_host['host_since'].dt.strftime('%Y-%m-%d')
        
        log.info(f"✅ df_listings - Filas: {df_listings.shape[0]:,}, Columnas: {df_listings.shape[1]}")
        
        # 4.8 Abstracción de amenities
        log.separator()
        log.info("4.8. Abstracción de df_amenities_listings")
        log.info("Se abstrae el df_amenities_listings del df_listings")
        
        df_amenities_listings = df_listings[['id', 'amenities']].copy()
        df_amenities_listings['amenities_str'] = df_amenities_listings['amenities'].astype(str)
        df_amenities_listings = df_amenities_listings.drop_duplicates(subset=['id', 'amenities_str']).drop(columns='amenities_str')
        df_listings = df_listings.drop(['amenities'], axis=1)
        
        log.info("Transformando amenities en lista de Python")
        df_amenities_listings['amenities'] = df_amenities_listings['amenities'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
        
        log.info("'Explotando' cada amenity para ser asignado uno a uno a su listing")
        df_amenities_listings = (
            df_amenities_listings[['id', 'amenities']]
            .explode('amenities')
            .reset_index(drop=True)
        )
        
        log.info(f"✅ df_amenities_listings - Filas: {df_amenities_listings.shape[0]:,}, Columnas: {df_amenities_listings.shape[1]}")
        
        # 4.9 Abstracción de catálogo de amenities
        log.separator()
        log.info("4.9. Abstracción de df_amenities")
        
        df_amenities_p = df_amenities_listings[['amenities']].drop_duplicates().reset_index(drop=True)
        log.info(f"✅ df_amenities preliminar - Filas: {df_amenities_p.shape[0]:,}")
        
        log.info("Limpieza de amenities repetidos y calidad de datos")
        df_amenities_p['amenities_clean'] = df_amenities_p['amenities'].apply(_clean_text)
        
        log.info(f"✅ df_amenities_p - Filas: {df_amenities_p.shape[0]:,}, Columnas: {df_amenities_p.shape[1]}")
        
        # 4.10 Transformación de amenities limpios
        log.separator()
        log.info("4.10. Transformación de amenities limpios a df_amenities_listings")
        log.info("Reemplazar amenities con versión limpia y renombrar 'id' a 'listing_id'")
        
        df_amenities_listings = (
            df_amenities_listings
            .merge(df_amenities_p, on='amenities', how='left')
            [['id', 'amenities_clean']]
            .rename(columns={'amenities_clean': 'amenities', 'id': 'listing_id'})
        )
        
        filas_antes = df_amenities_listings.shape[0]
        df_amenities_listings = df_amenities_listings[df_amenities_listings['amenities'] != ''].reset_index(drop=True)
        log.info(f"Eliminados {filas_antes - df_amenities_listings.shape[0]:,} amenities no válidos")
        
        log.info(f"✅ df_amenities_listings - Filas: {df_amenities_listings.shape[0]:,}, Columnas: {df_amenities_listings.shape[1]}")
        
        # 4.11 Creación de df_amenities final
        log.separator()
        log.info("4.11. Creación de df_amenities limpio y ajuste con IDs")
        log.info("Crear df_amenities limpio con amenities_id")
        
        df_amenities = df_amenities_listings[['amenities']].drop_duplicates().reset_index(drop=True)
        df_amenities.insert(0, 'amenities_id', df_amenities.index + 1)
        
        log.info(f"✅ df_amenities - Filas: {df_amenities.shape[0]:,}, Columnas: {df_amenities.shape[1]}")
        
        log.info("Reasignar amenities por amenities_id en df_amenities_listings")
        df_amenities_listings = (
            df_amenities_listings
            .merge(df_amenities, on='amenities', how='left')
            [['listing_id', 'amenities_id']]
        )
        
        log.info(f"✅ df_amenities_listings - Filas: {df_amenities_listings.shape[0]:,}, Columnas: {df_amenities_listings.shape[1]}")
        
        # 4.12 Resumen final
        log.separator()
        log.info("4.12. RESUMEN DE TABLAS GENERADAS:")
        log.info(f"✅ df_listings - Filas: {df_listings.shape[0]:,}, Columnas: {df_listings.shape[1]}")
        log.info(f"✅ df_host - Filas: {df_host.shape[0]:,}, Columnas: {df_host.shape[1]}")
        log.info(f"✅ df_verification - Filas: {df_verification.shape[0]:,}, Columnas: {df_verification.shape[1]}")
        log.info(f"✅ df_amenities_listings - Filas: {df_amenities_listings.shape[0]:,}, Columnas: {df_amenities_listings.shape[1]}")
        log.info(f"✅ df_amenities - Filas: {df_amenities.shape[0]:,}, Columnas: {df_amenities.shape[1]}")
        
        return (df_listings, df_host, df_verification, df_amenities_listings, df_amenities)
        
    except Exception as e:
        log.error(f"Error en _transformacion_listings: {str(e)}")
        raise


def _transformacion_reviews(df_reviews: pd.DataFrame, listings_ids: pd.Series, log: Logs):
    """Transforma reviews y extrae tabla de reviewers."""
    try:
        log.separator()
        log.info("4.13. Limpieza de df_reviews validando con df_listings")
        log.info("Se limpiará todos los reviews que no tengan un listing válido")
        
        filas_antes = df_reviews.shape[0]
        df_reviews = df_reviews[df_reviews['listing_id'].isin(listings_ids)]
        
        log.info(f"Eliminados {filas_antes - df_reviews.shape[0]:,} reviews sin listing válido")
        log.info(f"✅ df_reviews - Filas: {df_reviews.shape[0]:,}, Columnas: {df_reviews.shape[1]}")
        
        # 4.14 Abstracción de reviewers
        log.separator()
        log.info("4.14. Abstracción de df_reviewer")
        log.info("Se abstrae el df_reviewer del df_reviews")
        
        df_reviewer = df_reviews[['reviewer_id', 'reviewer_name']].drop_duplicates()
        
        log.info("Limpiando nombres de reviewers (seleccionando el más común por ID)")
        name_counts = (
            df_reviewer.groupby(['reviewer_id', 'reviewer_name'])
            .size()
            .reset_index(name='count')
        )
        most_common_names = (
            name_counts.sort_values(['reviewer_id', 'count'], ascending=[True, False])
            .drop_duplicates(subset=['reviewer_id'], keep='first')
        )
        df_reviewer = df_reviewer.drop(columns=['reviewer_name']).merge(
            most_common_names[['reviewer_id', 'reviewer_name']],
            on='reviewer_id',
            how='left'
        )
        
        log.info("Eliminando campo 'reviewer_name' de df_reviews")
        df_reviews = df_reviews.drop(['reviewer_name'], axis=1)
        
        log.info("Transformando campos de fecha a formato estándar")
        df_reviews['date'] = pd.to_datetime(df_reviews['date'])
        df_reviews['date'] = df_reviews['date'].dt.strftime('%Y-%m-%d')
        
        log.info(f"✅ df_reviews - Filas: {df_reviews.shape[0]:,}, Columnas: {df_reviews.shape[1]}")
        log.info(f"✅ df_reviewer - Filas: {df_reviewer.shape[0]:,}, Columnas: {df_reviewer.shape[1]}")
        
        return df_reviews, df_reviewer
        
    except Exception as e:
        log.error(f"Error en _transformacion_reviews: {str(e)}")
        raise


def _transformacion_calendar(df_calendar: pd.DataFrame, listings_ids: pd.Series, log: Logs):
    """Transforma el DataFrame de calendar."""
    try:
        log.separator()
        log.info("4.15. Limpieza de df_calendar validando con df_listings")
        log.info("Se limpiará todos los registros de calendar que no tengan un listing válido")
        
        filas_antes = df_calendar.shape[0]
        df_calendar = df_calendar[df_calendar['listing_id'].isin(listings_ids)]
        
        log.info(f"Eliminados {filas_antes - df_calendar.shape[0]:,} registros sin listing válido")
        log.info("Eliminando campos no necesarios")
        
        df_calendar = df_calendar.drop(['minimum_nights', 'maximum_nights', 'price', 'adjusted_price'], axis=1)
        
        log.info("Transformando campos de fecha a formato estándar")
        df_calendar['date'] = pd.to_datetime(df_calendar['date'])
        df_calendar['date'] = df_calendar['date'].dt.strftime('%Y-%m-%d')
        
        log.info(f"✅ df_calendar - Filas: {df_calendar.shape[0]:,}, Columnas: {df_calendar.shape[1]}")
        
        return df_calendar
        
    except Exception as e:
        log.error(f"Error en _transformacion_calendar: {str(e)}")
        raise


def _clean_text(a):
    
    if not isinstance(a, str):
        return ''
    
    a = a.lower().strip()
    a = a.replace('-', ' ')
    
    # Remover acentos
    a = ''.join(
        c for c in unicodedata.normalize('NFD', a)
        if unicodedata.category(c) != 'Mn'
    )
    
    a = ' '.join(a.split())
    return a