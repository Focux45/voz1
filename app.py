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
            background-color: #cacdf8; /* Azul */
            color: #ffffff; /* Letras blancas */
        }
            .mqtt-title {
            font-size: 24px; 
            font-weight: bold; 
            color: #333333; /* Texto oscuro */
            text-align: center; /* Centrar el texto */
        }
            .mqtt-description {
            font-size: 16px;
            color: #666666; /* Texto gris */
            text-align: center; /* Centrar el texto */
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
            background-color: #cacdf8; /* Azul */
            color: #ffffff; /* Letras blancas */
        }
            /* Contenedor para el título */
            .title-container {
                background-color: #cacdf8; 
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                width: 100vw; /* Asegura que el ancho sea igual al ancho total de la ventana */
                margin-left: -50vw; /* Centra el contenedor eliminando el margen del layout de Streamlit */
                margin-right: -50vw; /* Ajusta el margen derecho */
                position: relative; /* Permite ajustar el contenedor en relación al layout */
                left: 50%; /* Centra el contenedor */
                box-sizing: border-box; /* Incluye el padding dentro del ancho total */
        }
            .title-container p {
                text-align: center; /* Centra el texto horizontalmente */
                margin: 0 auto; /* Asegura un margen uniforme en ambos lados */
                line-height: 1.6; /* Mejora la separación entre líneas para mayor legibilidad */
                max-width: 80%; /* Limita el ancho del texto para que no abarque todo el contenedor */
                font-size: 16px; /* Ajusta el tamaño de fuente para mayor claridad */
        }
            .container {
                display: flex;
                flex-direction: row;
                align-items: center;
                background-color: #e0f7fa; /* Azul claro */
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
                border: 2px solid #000000; /* Borde negro */
                border-radius: 5px;
                text-decoration: none;
                transition: all 0.3s ease;
            }
            .button:hover {
                background-color: #cacdf8; /* Fondo azul claro */
                color: #ffffff; /* Texto blanco */
            }
            .tittle-model {
                background-color: #cacdf8; 
                padding: 20px;
                font-size: 18px;
                border-radius: 10px;
                margin-bottom: 20px;
                width: 100vw; /* Asegura que el ancho sea igual al ancho total de la ventana */
                margin-left: -50vw; /* Centra el contenedor eliminando el margen del layout de Streamlit */
                margin-right: -50vw; /* Ajusta el margen derecho */
                position: relative; /* Permite ajustar el contenedor en relación al layout */
                left: 50%; /* Centra el contenedor */
                box-sizing: border-box; /* Incluye el padding dentro del ancho total */
            }
            .tittle-model p {
            font-size: 16px;
            }
            .column-container {
        background-color: #d9f1ff; /* Fondo azul claro */
        padding: 20px; /* Espaciado interno */
        border-radius: 10px; /* Bordes redondeados */
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Sombra ligera */
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

# Obtener la ruta de la imagen
current_dir=os.path.dirname(os.path.abspath(__file__))
image_path=os.path.join(current_dir,"carrito.jpg")

# Crear columnas para dividir la imagen y el texto
col1, col2 = st.columns([1, 2])  # La imagen ocupa 1/3 del ancho, el texto 2/3


with col1:# Texto en la segunda columna
    st.markdown(
        """
        <div class="column-container">
            <h2 class="mqtt-title">Receptor MQTT</h2>
            <p class="mqtt-description">
                Este sistema recibe mensajes a través del protocolo MQTT, permitiendo comunicación rápida y segura para dispositivos IoT. 
                Un receptor MQTT es un componente clave en sistemas IoT que utiliza el protocolo Message Queuing Telemetry Transport (MQTT). 
                Este protocolo es ligero y eficiente, ideal para redes con recursos limitados o conexiones inestables, como dispositivos IoT o sensores en tiempo real.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

     

# Imagen en la primera columna
with col2:
 st.image(image_path)# Muestra la imagen
# Título para MQTT
#st.markdown('<h2 class="mqtt-title">Receptor MQTT</h2>', unsafe_allow_html=True)

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
    <div class="tittle-model">
        <h3 class="main-title">Modelos de carros que han usado nuestro servicio</h3>
         <p class="subheader">Los servicios de carros han sido esenciales para garantizar el rendimiento y la seguridad de vehículos de diversas marcas reconocidas. Chevrolet, con modelos icónicos como el Chevrolet Spark y el Camaro, ofrece opciones que van desde compactos económicos hasta deportivos de alto rendimiento. Mazda destaca con su tecnología Skyactiv y diseños modernos, visibles en modelos como el Mazda 3 y el CX-5, ideales para quienes buscan eficiencia y estilo. Ford, por su parte, ha sido líder con modelos como el Mustang y la F-150, combinando potencia y durabilidad. BMW, símbolo de lujo y alto desempeño, es conocido por su Serie 3 y la línea X de SUV, que brindan una experiencia de conducción premium.
</p>
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
    if st.button("prev"):
        prev_image()

with col2:
    st.image(images[st.session_state.index], caption=f"Imagen {st.session_state.index + 1}", use_column_width=True)

with col3:
    if st.button("next"):
        next_image()

# Mostrar el índice actual en el slider
st.write(f"Imagen {st.session_state.index + 1} de {len(images)}")

# Obtener la ruta absoluta de la imagen
current_dir=os.path.dirname(os.path.abspath(__file__))
image_path=os.path.join(current_dir,"mazda.jpg")


# Contenedor con imagen y texto
img_col, text_col = st.columns([1, 2])  # Usamos nombres diferentes para las columnas

with img_col:
    st.image(image_path, caption="On Car")  # Mostrar la imagen

with text_col:
    st.markdown(
        """
        <div class="text-container">
            <h2>OnStar siempre on para protegerte</h2>
            <p>OnStar® es un servicio exclusivo que te ofrece seguridad y practicidad las 24 horas dentro y fuera de tu Chevrolet. 
            Cuenta con diagnóstico del vehículo, comandos remotos como abrir y cerrar puertas a distancia y mucho más.</p>
            <a href="#" class="button">Explora OnStar</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
