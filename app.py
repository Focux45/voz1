import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
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
        client.connect("broker.mqttdashboard.com", 1883, 60)
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



st.title("🏎️🏎️ DETECTRON 2.0 🏎️🏎️")
st.subheader("Control de voz del sensor")

image = Image.open('melo.png')

st.image(image, width= 400)




st.write("Toca el Botón para encender el sensor de reversa ")

stt_button = Button(label=" Inicio ", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act1":result.get("GET_TEXT").strip()})
        ret= client1.publish("control_juan", message)

    
    try:
        os.mkdir("temp")
    except:
        pass

st.title("Receptor MQTT")

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




st.write("Modelos de carros que han usado nuestro servicio")


image_paths = ['bmw.jpg', 'chevro.jpeg', 'ford.png', 'mazda.jpg', 'renault.jpg']
images = [Image.open(img_path) for img_path in image_paths]

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

# Botones para navegar entre las imágenes
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("Anterior"):
        prev_image()
with col2:
    st.image(images[st.session_state.index], caption=f"Imagen {st.session_state.index + 1}", use_column_width=True)
with col3:
    if st.button("Siguiente"):
        next_image()


