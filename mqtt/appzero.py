from guizero import App, Text, PushButton, TextBox
import paho.mqtt.client as client
from paho import mqtt

import os

client_name = "gpf_python"
broker_address = "8f7d568006ab499c99e5a16b885e2d05.s2.eu.hivemq.cloud"
app = App(title="Hello world")
testo = Text(app, text="Welcome to the app")
testo1 = Text(app, text="")

# app.bg = (251, 251, 208)
username = os.environ.get("MQTT_NODE_USER")
pwd = os.environ.get("MQTT_NODE_PWD")


def on_message(client, userdata, message):
    global testo1
    print("On Message")
    testo1.value = str("")
    testo1.value = str(message.payload.decode("utf-8"))
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_connect(client, userdata, flags, rc):
    print("On Connect")
    print("Connected with result code " + str(rc))


def on_disconnect(client, userdata, rc):
    print("On Disconnect")
    if rc != 0:
        print("Unexpected disconnection.")


def on_publish(client, userdata, mid):
    print("On Publish")
    print("Messaggio Pubblicato " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribe")
    print("Sottoscritto con Qos " + str(granted_qos))


client = client.Client(client_name)
client.on_connect = on_connect  # attach function to callback
client.on_disconnect = on_disconnect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.on_publish = on_publish  # attach function to callback
client.on_subscribe = on_subscribe  # attach function to callback
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(username, pwd)
# client.connect_async(broker_address, port=1883, keepalive=60, bind_address="")
client.connect(broker_address, port=8883, keepalive=60, bind_address="")


def stop_loop():
    global client
    print("Stop Loop")
    client.loop_stop()  # stop the loop


button = PushButton(app, stop_loop, text="Stop Loop")


def start_loop():
    global client
    print("Start Loop")
    client.loop_start()  # start the loop
    ret = client.subscribe("#", 0)
    print("Sottoscritto con ret = " + str(ret))


button = PushButton(app, start_loop, text="Start Loop & Subscribe")

my_textbox = TextBox(app, "Stringa da pubblicare", width=25, scrollbar=True)


def pubblica():
    print("Pubblica")
    ret = client.publish("Status", payload=my_textbox.value, qos=0, retain=False)
    print("Pubblicato con ret = " + str(ret))


button = PushButton(app, pubblica, text="Pubblica")


def pulisci():
    global testo1
    testo1.value = str("")


button = PushButton(app, pulisci, text="Pulisci")


def chiudi():
    global client
    client.disconnect()
    app.destroy()


button = PushButton(app, chiudi, text="Chiudi")

# client.publish("Status", payload="Lampada/On", qos=0, retain=False)


app.display()
