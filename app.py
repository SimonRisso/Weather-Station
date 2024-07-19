import streamlit as st
import pandas as pd
from class_firebase_database import FirebaseDB
import time
import os
from dotenv import load_dotenv
st.set_page_config(page_title="Estación Meteorológica", layout="centered")

# Cargar variables de entorno
load_dotenv()

# Configuración de Firebase
path = os.getenv('FIREBASE_CREDENTIALS_PATH')
url = os.getenv('FIREBASE_DATABASE_URL')
fb_db = FirebaseDB(path, url)

# Función para obtener los datos de Firebase y convertirlos en un DataFrame
def get_data():
    data = fb_db.read_record("/datos")
    if data:
        # Crear DataFrame y transponer para que las claves sean las filas
        df = pd.DataFrame(data).T
        
        # Convertir el índice a datetime
        df.index = pd.to_datetime(df.index)
        
        # Eliminar la columna 'timestamp'
        df = df.drop(columns=['timestamp'], errors='ignore')
        
        return df
    else:
        return pd.DataFrame()
    
# print("Columnas disponibles:", get_data())
    
def get_latest_data():
    df = get_data()
    if not df.empty:
        return df.iloc[-1]
    return pd.Series()  # Retornar una Serie vacía en lugar de None

# Configurar la página principal de Streamlit
# st.title("Estación Meteorológica", anchor=False)
st.markdown(f"""
      <div style="text-align: center;">
          <h1 style="font-size: 48px; font-weight: bold;">Estación Meteorológica</h1>
      </div>
      """, unsafe_allow_html=True)

# Bucle de actualización
while True:
  # Obtener los datos actuales de temperatura y humedad
  latest_data = get_latest_data()
  if not latest_data.empty:
      temperature = latest_data['temperature']
      humidity = latest_data['humidity']
  else:
      temperature = "N/A"
      humidity = "N/A"

  # Mostrar los datos actuales en grande
  st.markdown(f"""
      <div style="text-align: center;">
          <p style="font-size: 48px; font-weight: bold;">{temperature} °C</p>
          <p style="font-size: 48px; font-weight: bold;">{humidity} %</p>
      </div>
      """, unsafe_allow_html=True)

  # Obtener los datos de Firebase
  df = get_data()

  if not df.empty:
    st.markdown("""
            <div style="text-align: center;">
                <h2>Historial de datos:</h2>
                <div style="display: inline-block; text-align: left;">
                    {0}
                </div>
            </div>
            """.format(df.tail(10).to_html(classes='dataframe', header=True, index=True)), unsafe_allow_html=True)  # Mostrar las últimas filas del DataFrame

      # Mostrar el historial de datos
    st.write("Gráfico:")
    st.line_chart(df[['temperature', 'humidity']])

      # Calcular y mostrar el ranking de temperaturas más altas en los últimos 5 días
    last_5_days = df[df.index >= (pd.Timestamp.now() - pd.Timedelta(days=5))]
    if not last_5_days.empty:
        top_temps = last_5_days['temperature'].astype(float).nlargest(5)
        st.markdown("""
            <div style="text-align: center;">
                <h2>Ranking de temperaturas más altas en los últimos 5 días:</h2>
                <div style="display: inline-block; text-align: left;">
                    {0}
                </div>
            </div>
            """.format(top_temps.to_frame().to_html(classes='dataframe', header=True, index=True)), unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center;">
                <h2>Ranking de temperaturas más altas en los últimos 5 días:</h2>
                <p>No hay datos suficientes para los últimos 5 días.</p>
            </div>
            """, unsafe_allow_html=True)
  else:
      st.write("No se encontraron datos en Firebase.")
  
  # Esperar 10 segundos antes de actualizar
  time.sleep(10)
  st.rerun()

  # Ejecutar la aplicación con Streamlit
if name == 'main':
    st.set_page_config(page_title="Estación Meteorológica", layout="wide")
    st.write("Iniciando aplicación...")