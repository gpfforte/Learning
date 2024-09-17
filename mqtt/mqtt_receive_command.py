import paho.mqtt.client as mqtt  # import the client1
import time
import certifi
import os
username = os.environ.get("MQTT_NODE_USER")
pwd = os.environ.get("MQTT_NODE_PWD")
############


def on_message(client, userdata, message):
    print("On Message")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_connect(client, userdata, flags, rc):
    print("On Connect")
    print("Connected with result code "+str(rc))


def on_disconnect(client, userdata, rc):
    print("On Disconnect")
    if rc != 0:
        print("Unexpected disconnection.")


def on_publish(client, userdata, mid):
    print("On Publish")
    print("Messaggio Pubblicato "+str(mid))


def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribe")
    print("Sottoscritto con Qos "+str(granted_qos))


########################################
broker_address = "node02.myqtthub.com"
# broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("gpf_forte@hotmail.com")  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_disconnect = on_disconnect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.on_publish = on_publish  # attach function to callback
client.on_subscribe = on_subscribe  # attach function to callback
print("connecting to broker")
client.username_pw_set(username, pwd)
client.tls_set(certifi.where())
client.connect(broker_address, port=8883)  # connect to broker
client.loop_start()  # start the loop
topic = "Command"
print("Subscribing to topic", topic)
ret = client.subscribe(topic, 0)
print("Sottoscritto con ret = " + str(ret))
time.sleep(20)  # wait
client.loop_stop()  # stop the loop
