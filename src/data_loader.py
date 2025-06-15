import os
import pandas as pd
import yfinance as yf

# Ruta al directorio donde se guardarán los datos crudos
RAW_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw"))

# Diccionario de tickers para activos representativos de la BVC
TICKERS_BVC = {
    "Ecopetrol": "EC",
    "Bancolombia": "CIB",
    "Grupo Aval": "AVAL",
    "ISA": "ISA",
    "Grupo Sura": "GIVSY"
}

def descargar_datos(ticker, inicio="2022-01-01", fin="2025-01-01", guardar_csv=True):
    """
    Descarga datos históricos desde Yahoo Finance para un ticker específico.
    
    Args:
        ticker (str): Símbolo del activo (ej. 'EC').
        inicio (str): Fecha inicial (formato YYYY-MM-DD).
        fin (str): Fecha final (formato YYYY-MM-DD).
        guardar_csv (bool): Si True, guarda el CSV en /data/raw/.
    
    Returns:
        DataFrame: Datos descargados.
    """
    print(f"Descargando datos para {ticker} desde {inicio} hasta {fin}...")
    datos = yf.download(ticker, start=inicio, end=fin)

    if datos.empty:
        print(f"⚠️ No se encontraron datos para {ticker}.")
        return None

    if guardar_csv:
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        ruta_salida = os.path.join(RAW_DATA_DIR, f"{ticker}.csv")
        datos.to_csv(ruta_salida)
        print(f"✅ Datos guardados en: {ruta_salida}")

    return datos


def cargar_datos_activo(ticker):
    """
    Carga los datos históricos guardados previamente en un CSV.
    
    Args:
        ticker (str): Símbolo del activo (sin ".csv").
    
    Returns:
        DataFrame: Datos cargados desde el archivo.
    
    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    archivo = os.path.join(RAW_DATA_DIR, f"{ticker}.csv")
    if os.path.exists(archivo):
        return pd.read_csv(archivo, index_col=0, parse_dates=True)
    else:
        raise FileNotFoundError(f"No se encontró el archivo para el ticker: {ticker}")
