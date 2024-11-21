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

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)
    
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




broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("control_juan")
client1.on_message = on_message


# Configuración de la página
st.set_page_config(
    page_title="DETECTRON 2.0",
    page_icon="🏎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Estilos CSS personalizados
st.markdown(
    """
    <style>
        .css-fg4pbf {
            background: linear-gradient(to bottom, #ffffff, #0000FF); /* Gradiente blanco a azul */
            background-attachment: fixed; /* Fondo fijo */
            padding: 20px; /* Añade algo de padding para que sea más visible */
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #000000; /* Negro */
            margin-bottom: 10px;
        }
        .subheader {
            font-size: 18px;
            text-align: center;
            color: #000000; /* Negro */
            margin-bottom: 30px;
        }
        .center {
            text-align: center;
        }
        .custom-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            color: #000000; /* Letras negras */
            background-color: #ffffff; /* Fondo blanco */
            border: 2px solid #000000; /* Borde negro */
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s; /* Transición suave */
        }
        .custom-button:hover {
            background-color: #0000FF; /* Azul */
            color: #ffffff; /* Letras blancas */
        }
        .mqtt-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: #000000; /* Negro */
            margin-top: 40px;
        }
            .stButton > button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            color: #000000; /* Letras negras */
            background-color: #ffffff; /* Fondo blanco */
            border: 2px solid #000000; /* Borde negro */
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
    }
    .stButton > button:hover {
            background-color: #0000FF; /* Azul */
            color: #ffffff; /* Letras blancas */
    }
    /* Contenedor para el título */
        .title-container {
            background-color: #cacdf8; /* Azul claro */
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    .container {
        display: flex;
        flex-direction: row;
        align-items: center;
        background-color: #f4f4f4; /* Fondo gris claro */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra ligera */
    }
    .image-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .image-container img {
        max-width: 100%;
        border-radius: 8px;
    }
    .text-container {
        flex: 2;
        padding-left: 20px;
    }
    .text-container h2 {
        font-size: 24px;
        font-weight: bold;
        color: #333333; /* Texto oscuro */
        margin-bottom: 10px;
    }
    .text-container p {
        font-size: 16px;
        color: #666666; /* Texto gris */
        margin-bottom: 20px;
    }
     .button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: #000000; /* Texto negro */
        background-color: transparent;
        border: 2px solid #af872f; /* Borde dorado */
        border-radius: 5px;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .button:hover {
        background-color: #af872f; /* Fondo dorado */
        color: #ffffff; /* Texto blanco */
    }

    </style>
    """,
    unsafe_allow_html=True,
)
# Encabezado principal dentro de un contenedor
st.markdown(
    """
    <div class="title-container">
        <h1 class="main-title">🏎🏎 DETECTRON 2.0 🏎🏎</h1>
        <p class="subheader">Control de voz del sensor</p>
    </div>
    """,
    unsafe_allow_html=True,
)
# Encabezado principal
#st.markdown('<h1 class="main-title">🏎🏎 DETECTRON 2.0 🏎🏎</h1>', unsafe_allow_html=True)
#st.markdown('<p class="subheader">Control de voz del sensor</p>', unsafe_allow_html=True)

# Mostrar el contenedor de la imagen
image = Image.open('melo.png')  # Asegúrate de que 'melo.png' esté en el directorio
st.image(image, width=400,use_column_width=False, caption="")
st.markdown(
    """
    <div class="image-container">
    
    </div>
    """,
    unsafe_allow_html=True,
)
# Mostrar imagen
#image = Image.open('melo.png')  # Asegúrate de que el archivo 'melo.png' esté en el directorio
#st.image(image, width=400, use_column_width=False, caption="")

# Texto y botón
st.markdown(
    """
    <div class="center">
        <p>Toca el botón para encender el sensor de reversa</p>
        <a href="https://crutrv5uanw72zk6druncx.streamlit.app/" class="custom-button">Ir al control de voz</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Título para MQTT
st.markdown('<h2 class="mqtt-title">Receptor MQTT</h2>', unsafe_allow_html=True)

if st.button("Recibir"):
    with st.spinner('Esperando mensaje...'):
        mensaje = get_mqtt_message()
        if mensaje:
            st.write("Mensaje recibido:", mensaje)
        else:
            st.write("No se recibió mensaje")

with st.sidebar:
  st.subheader("selecciona tu marca de carro")
  mod_radio = st.radio(
    "Escoge una marca", 
    ("Chevrolet", "Renault","Ford","Mazda","Kia", "Opel", "BMW", "Mitsubishi", "MINI")
  )

col1, col2 = st.columns(2)

with col1:
  st.subheader("Ayuda")
  st.write("Se te dificulta reversar?")
  resp = st.checkbox("Si, se me dificulta")
  if resp:
    st.write("Nosotros te ayudamos")

with col2:
  st.subheader("Transmisión del vehiculo")
  modo = st.radio("Tu carro es mecanico o automatico", ("automatico", "mecanico"))
  if modo == "automatico":
    st.write("Recibido")
  if modo == "mecanico":
    st.write("Recibido")



# Título de la aplicación
#st.write("Modelos de carros que han usado nuestro servicio")
st.markdown(
    """
    <div class="title-">
        <h3 class="main-title">Modelos de carros que han usado nuestro servicio</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
# Rutas de las imágenes
image_paths = ['bmw.jpg', 'chevro.jpeg', 'ford.png', 'mazda.jpg', 'renault.jpg']
images = [Image.open(img_path) for img_path in image_paths]

# Establecer el índice inicial en la sesión
if 'index' not in st.session_state:
    st.session_state.index = 0

# Funciones para avanzar y retroceder
def next_image():
    if st.session_state.index < len(images) - 1:
        st.session_state.index += 1

def prev_image():
    if st.session_state.index > 0:
        st.session_state.index -= 1

# Botones para navegar entre las imágenes
col1, col2, col3 = st.columns([1, 5, 1])

with col1:
    if st.button("Anterior"):
        prev_image()

with col2:
    st.image(images[st.session_state.index], caption=f"Imagen {st.session_state.index + 1}", use_column_width=True)

with col3:
    if st.button("Siguiente"):
        next_image()

# Mostrar el índice actual en el slider
st.write(f"Imagen {st.session_state.index + 1} de {len(images)}")

# Contenido HTML
st.markdown(
    """
    <div class="container">
        <div class="image-container">
        </div>
        <div class="text-container">
            <h2>Siempre on para protegerte</h2>
            <p>Es un servicio exclusivo que te ofrece seguridad y practicidad las 24 horas dentro y fuera de tu Chevrolet. 
            Cuenta con diagnóstico del vehículo, comandos remotos como abrir y cerrar puertas a distancia y mucho más.</p>
            <a href="#" class="button">Explora</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
