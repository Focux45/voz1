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

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("control_juan")
client1.on_message = on_message



st.title("🏎️🏎️ DETECTRON 2.0 🏎️🏎️")
st.subheader("Control de voz del sensor")

image = Image.open('melo.png')

st.image(image, width= 400)




st.write("Toca el Botón y habla ")

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
  resp = st.checkbox("Preguntele a chatgpt")
  if resp:
    st.write("Preste atención a la clase")

with col2:
  st.subheader("Carro")
  modo = st.radio("Tu carro es mecanico o automatico", ("Chevrolet", "Renault","Ford"))
  if modo == "Chevrolet":
    st.write("Es una marca interesante")
  if modo == "Renault":
    st.write("Es una marca francesa")
  if modo == "Ford":
    st.write("La marca mas vendida en los estados unidos")
