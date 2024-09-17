import paho.mqtt.client as mqtt  # import the client1
import time
import ssl
import certifi
import os
from servizio import log_setup
from logging import DEBUG

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

username = os.environ.get("MQTT_NODE_USER")
pwd = os.environ.get("MQTT_NODE_PWD")

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)


############
def on_connect(client, userdata, flags, rc, properties=None):
    print("connecting to broker")
    print(flags)
    print(client._client_id)
    print("Connection returned " + str(rc))
    if rc == 0:
        print("Brocker Connected")


def on_disconnect(client, userdata, rc):
    print("Client Got Disconnected")


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")).strip())
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_message_from_kitchen(client, userdata, message):
    print("Message Received from Kitchen: " + message.payload.decode())


########################################
# broker_address = "node02.myqtthub.com"
broker_address = "8f7d568006ab499c99e5a16b885e2d05.s2.eu.hivemq.cloud"
# broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("gpf_python")  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.on_disconnect = on_disconnect  # attach function to callback
client.username_pw_set(username, pwd)

# configure TLS connection
# client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1)
# client.tls_insecure_set(False)
# port = 8883
# cert_reqs=ssl.CERT_NONE

# client.tls_set()
# client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)
print(certifi.where())
client.tls_set(certifi.where())
argomento_sub = "gpf/#"
argomento_pub = "gpf/casa/lampada"


def main():
    client.connect(broker_address, port=8883)  # connect to broker
    client.loop_start()  # start the loop
    time.sleep(3)  # wait for the connection
    if client.is_connected():
        client.subscribe("KitchenTopic", qos=0)
        client.message_callback_add("KitchenTopic", on_message_from_kitchen)
        print("client.is_connected()", client.is_connected())
        print("Subscribing to topic", argomento_sub)
        # client.unsubscribe(argomento_sub)
        client.subscribe(argomento_sub, qos=0)
        time.sleep(5)
        print(f"Publishing message to topic {argomento_pub}")
        # Se qos di entrambi è 1, non vedo il messaggio sottoscritto, se invece è 0 nel sottoscrittore, allora lo vedo. Probabilmente perché
        # nel primo caso non riesce a dare la conferma al server.
        client.publish(argomento_pub, "OFF", qos=1, retain=False)
        new_topic = "KitchenTopic"
        print(f"Publishing message to topic {new_topic}")
        client.publish(new_topic, "Ciao", qos=1, retain=False)
        time.sleep(5)  # wait
    client.loop_stop()  # stop the loop


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
