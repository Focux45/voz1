import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import paho.mqtt.client as mqtt
import json
from gtts import gTTS
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Detectron 2.0",
    page_icon="🚗",
    layout="wide",
)

# Estilo personalizado
st.markdown("""
    <style>
    .header-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #003366;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 20px;
        text-align: center;
        color: #0066cc;
        margin-bottom: 30px;
    }
    .main-button {
        background-color: #0056b3;
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
    }
    .main-button:hover {
        background-color: #004494;
        color: #e6e6e6;
    }
    .mqtt-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ccc;
        margin-top: 20px;
    }
    .sidebar-header {
        font-size: 18px;
        font-weight: bold;
        color: #003366;
    }
    .custom-radio {
        font-size: 16px;
        color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# Título y subtítulo
st.markdown('<div class="header-title">Detectron 2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Sistema avanzado de sensores de reversa con control de voz</div>', unsafe_allow_html=True)

# Imagen principal
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    image = Image.open('melo.png')  # Cambia 'melo.png' por el nombre correcto de tu archivo.
    st.image(image, caption="Tu copiloto inteligente", use_column_width=True)

# Función para publicar mensajes MQTT
def on_publish(client, userdata, result):
    """Callback al publicar un mensaje."""
    print("El dato ha sido publicado\n")
    pass

# Función para manejar mensajes MQTT
def on_message(client, userdata, message):
    """Callback al recibir un mensaje."""
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Función para recibir un mensaje MQTT
def get_mqtt_message():
    """Función simple para recibir un mensaje MQTT"""
    mensaje_recibido = None

    def on_message(client, userdata, message):
        nonlocal mensaje_recibido
        mensaje_recibido = message.payload.decode()

    # Crear y configurar cliente MQTT
    client = mqtt.Client()
    client.on_message = on_message

    try:
        # Conectar y suscribir
        client.connect("157.230.214.127", 1883, 60)
        client.subscribe("app_")

        # Esperar mensaje
        client.loop_start()
        time.sleep(3)  # Espera 3 segundos
        client.loop_stop()

        return mensaje_recibido

    except Exception as e:
        return f"Error: {e}"

# Configuración inicial del cliente MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("control_juan")
client1.on_message = on_message

# Sección de recepción MQTT
st.markdown('<div class="mqtt-section">', unsafe_allow_html=True)
st.write("## Receptor MQTT")
if st.button("📡 Recibir mensaje"):
    with st.spinner('Esperando mensaje del servidor...'):
        mensaje = get_mqtt_message()
        if mensaje:
            st.success(f"Mensaje recibido: {mensaje}")
        else:
            st.warning("No se recibió ningún mensaje.")
st.markdown('</div>', unsafe_allow_html=True)

# Barra lateral
with st.sidebar:
    st.markdown('<div class="sidebar-header">Configuración del vehículo</div>', unsafe_allow_html=True)
    st.subheader("Selecciona la marca")
    marca = st.radio(
        "Marcas disponibles:",
        ["Chevrolet", "Renault", "Ford", "Mazda", "Kia", "Opel", "BMW", "Mitsubishi", "MINI"],
        key="marca_radio"
    )
    st.write(f"Marca seleccionada: *{marca}*")

# Galería de imágenes con navegación
images = ["imagen1.png", "imagen2.png", "imagen3.png"]  # Coloca aquí tus imágenes reales

# Establecer el índice inicial
if 'index' not in st.session_state:
    st.session_state.index = 0

# Funciones para avanzar y retroceder
def next_image():
    if st.session_state.index < len(images) - 1:
        st.session_state.index += 1

def prev_image():
    if st.session_state.index > 0:
        st.session_state.index -= 1

# Navegación entre imágenes
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("Anterior"):
        prev_image()
with col2:
    st.image(images[st.session_state.index], caption=f"Imagen {st.session_state.index + 1}", use_column_width=True)
with col3:
    if st.button("Siguiente"):
        next_image()
