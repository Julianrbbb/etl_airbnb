import pandas as pd
import pyodbc
import numpy as np

__all__ = ['conectar_sql', 'cargar_data_frame']

def conectar_sql():
    try:
        conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-Q68QGU3\\JUSERVER;"
            "DATABASE=AirbnbMexico;"
            "UID=Universidad;"
            "PWD=itm2025*;"
        )
        print("✅ Conexión exitosa a MongoDB")
        return conexion
    except pyodbc.Error as e:
        raise Exception(f"❌ Error de conexión: {e}")

def cargar_data_frame(conexion, df: pd.DataFrame, table_name):
    _crear_tabla(conexion, df, table_name)
    _insertar_data(conexion, df, table_name)

def _crear_tabla(conexion, df, table_name):
    cursor = conexion.cursor()

    check_query = f"""
        IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}')
            SELECT 1 AS existe
        ELSE
            SELECT 0 AS existe
    """
    cursor.execute(check_query)
    existe = cursor.fetchone()[0]

    # 2️⃣ Si no existe, crearla
    if existe:
        print(f"\n✅ Tabla [{table_name}] ya existe. Limpiando datos...")
        cursor.execute(f"TRUNCATE TABLE [{table_name}];")
        conexion.commit()
        print(f"✅ Tabla [{table_name}] limpiada.")
        return

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
    columns_sql = ",\n  ".join(columns)
    query = f'CREATE TABLE [{table_name}] (\n  {columns_sql}\n);'

    cursor.execute(query)
    conexion.commit()

    print(f"\n✅ Tabla [{table_name}] creada correctamente en SQL Server.")

def _insertar_data(conexion, df, table_name):
    cursor = conexion.cursor()

    df.apply(lambda col: col.map(_to_python_value))

    cols = ", ".join(f"[{c}]" for c in df.columns)
    placeholders = ", ".join("?" for _ in df.columns)
    sql = f"INSERT INTO [{table_name}] ({cols}) VALUES ({placeholders})"

    data = [tuple(None if pd.isna(x) else x for x in row) for row in df.to_numpy()]

    try:
        cursor.executemany(sql, data)
        conexion.commit()
        print(f"✅ {len(df)} filas insertadas en [{table_name}] correctamente.")
    except Exception as e:
        print(f"❌ Error al insertar datos en [{table_name}]: {e}")
        conexion.rollback()

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