import paho.mqtt.client as mqtt  # import the client1
import time
import os
username = os.environ.get("MQTT_RASPI_USER")
pwd = os.environ.get("MQTT_RASPI_PWD")
############


def on_message(client, userdata, message):
    print("message received =", str(message.payload.decode("utf-8")))
    print("message topic =", message.topic)
    print("message qos =", message.qos)
    print("message retain flag =", message.retain)


########################################
broker_address = "192.168.1.99"
# broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client(client_id="P1", protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)  # create new instance
client.on_message = on_message  # attach function to callback
print("connecting to broker")
# client.username_pw_set(username, pwd)
client.connect(broker_address, 1883)  # connect to broker
client.loop_start()  # start the loop
print("Subscribing to topic", "Status")
client.subscribe("Status")
print("Publishing message to topic", "Status")
client.publish("Status", "ON")
time.sleep(4)  # wait
client.loop_stop()  # stop the loop
