"""
Módulo de Procesamiento y Limpieza de Leads
Completa las funciones indicadas para limpiar, validar y generar métricas del dataset.
"""
import os
import pandas as pd
import requests

DATA_IN = os.path.join(os.path.dirname(__file__), "..", "data", "leads.csv")
DATA_OUT = os.path.join(os.path.dirname(__file__), "..", "data", "leads_limpios.csv")

def cargar_datos() -> pd.DataFrame:
    """1. Cargar el dataset crudo."""
    df = pd.read_csv(DATA_IN)
    print(f"Total registros cargados: {len(df)}")
    return df



# new 

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    2. Limpieza de datos:
       - Eliminar registros duplicados considerando el campo email.
       - Descartar registros con email vacío.
       - Normalizar los valores de estatus a: NUEVO, CONTACTADO, EN_SEGUIMIENTO, CONVERTIDO, PERDIDO.
       - Rellenar valores nulos en la columna presupuesto con 0.
    """
    df_limpio = df.copy()
    
    # 1. Limpiar email (convertir nulos a vacíos, aplicar strip y minúsculas)
    df_limpio['email'] = df_limpio['email'].fillna('').astype(str).str.strip().str.lower()
    
    # 2. Descartar registros con email vacío
    df_limpio = df_limpio[df_limpio['email'] != '']
    
    # 3. Eliminar duplicados por email (conservando el primer registro)
    df_limpio = df_limpio.drop_duplicates(subset=['email'], keep='first')
    
    # 4. Diccionario de mapeo para normalizar estatus
    estatus_map = {
        'nuevo': 'NUEVO',
        'contactado': 'CONTACTADO',
        'en seguimiento': 'EN_SEGUIMIENTO',
        'seguimiento': 'EN_SEGUIMIENTO',
        'convertido': 'CONVERTIDO',
        'cerrado ganado': 'CONVERTIDO',
        'perdido': 'PERDIDO',
        'descartado': 'PERDIDO',
        'no interesado': 'PERDIDO'
    }
    
    # Aplicar normalización de estatus (quitando espacios y convirtiendo a minúsculas antes de mapear)
    df_limpio['estatus'] = (
        df_limpio['estatus']
        .fillna('')
        .astype(str)
        .str.strip()
        .str.lower()
        .map(lambda val: estatus_map.get(val, val.upper()))
    )
    
    # 5. Convertir presupuesto a numérico y reemplazar valores nulos con 0
    df_limpio['presupuesto'] = pd.to_numeric(df_limpio['presupuesto'], errors='coerce').fillna(0)
    
    return df_limpio


#new

def generar_resumen(df: pd.DataFrame):
    """
    3. Imprimir métricas en consola:
       - Total de prospectos limpios.
       - Cantidad de prospectos por origen.
       - Cantidad de prospectos por estatus normalizado.
    """
    print("\n--- RESUMEN DE LEADS ---")
    print(f"Total de prospectos limpios: {len(df)}")
    
    print("\nProspectos por origen:")
    print(df['origen'].value_counts().to_string())
    
    print("\nProspectos por estatus:")
    print(df['estatus'].value_counts().to_string())


def exportar_datos(df: pd.DataFrame):
    """4. Guardar dataset limpio listo para base de datos."""
    df.to_csv(DATA_OUT, index=False)
    print(f"\nDataset limpio guardado en: {DATA_OUT}")

def enviar_muestra_api(df: pd.DataFrame, limite: int = 5):
    """
    5. Consumo de API:
       - Tomar una muestra de los primeros `limite` prospectos.
       - Enviar una petición POST a la API (http://127.0.0.1:8000/api/leads)
         utilizando el encabezado 'Authorization: Bearer atlas-token-2026'.
    """
    url = "http://127.0.0.1:8000/api/leads"
    headers = {
        "Authorization": "Bearer atlas-token-2026",
        "Content-Type": "application/json"
    }
    
    muestra = df.head(limite)
    print(f"\n--- ENVIANDO MUESTRA DE {len(muestra)} LEADS A LA API ---")
    
    for _, row in muestra.iterrows():
        payload = {
            "id": int(row["id"]),
            "nombre": str(row["nombre"]),
            "email": str(row["email"]),
            "telefono": str(row["telefono"]) if pd.notna(row["telefono"]) else "",
            "origen": str(row["origen"]),
            "fecha_registro": str(row["fecha_registro"]),
            "estatus": str(row["estatus"]),
            "presupuesto": float(row["presupuesto"]),
            "desarrollo_id": int(row["desarrollo_id"]),
            "comentarios": str(row["comentarios"]) if pd.notna(row["comentarios"]) else None
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f"Lead ID {payload['id']} - Status Code: {response.status_code} - Respuesta: {response.json()}")
        except Exception as e:
            print(f"Error al enviar Lead ID {payload['id']}: {e}")

