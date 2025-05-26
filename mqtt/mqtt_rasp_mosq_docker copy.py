import paho.mqtt.client as mqtt  # Importa il client Paho MQTT
import time
import random # Per generare un ID client unico

# --- Callback Functions ---

def on_connect(client, userdata, flags, rc, properties=None):
    """
    Callback che viene chiamato quando il client si connette al broker.
    Per CallbackAPIVersion.VERSION2:
    rc (return code) è ora reason_code
    flags è rimosso (dalla documentazione standard per on_connect in v2, ma Paho lo passa ancora)
    properties è aggiunto
    """
    if rc == 0:
        print("Connesso al broker MQTT! (Codice di ritorno: {})".format(rc))
        # Sottoscrivi al topic qui. Questo assicura che la sottoscrizione
        # venga ristabilita se la connessione cade e si riconnette.
        client.subscribe("Status", qos=1) # Sottoscrivo con QoS 1
        print("Sottoscritto al topic 'Status'")
    else:
        print("Fallita la connessione al broker! Codice di ritorno: {}".format(rc))

def on_message(client, userdata, message):
    """
    Callback che viene chiamato quando un messaggio viene ricevuto dal broker.
    Per CallbackAPIVersion.VERSION2:
    'message' è l'oggetto completo del messaggio, non 'msg'.
    """
    print(f"Messaggio ricevuto: '{message.payload.decode('utf-8')}'")
    print(f"Topic: '{message.topic}'")
    print(f"QoS: {message.qos}")
    print(f"Flag Retain: {message.retain}")

def on_publish(client, userdata, mid, reason_code, properties):
    """
    Callback che viene chiamato quando un messaggio pubblicato è stato confermato dal broker.
    Per CallbackAPIVersion.VERSION2, la firma include reason_code e properties.
    mid è l'oggetto completo del messaggio (message_info).
    """
    print(f"Messaggio pubblicato con ID: {mid}, Reason Code: {reason_code}")
    # Puoi anche accedere a properties se necessario, ad esempio:
    # if properties:
    #     print(f"Properties: {properties}")

def on_disconnect(client, userdata, rc, flags, properties):
    """
    Callback che viene chiamato quando il client si disconnette dal broker.
    Per CallbackAPIVersion.VERSION2, 'rc' è un oggetto ReasonCode (o DisconnectFlags).
    Non ha l'attributo 'value' direttamente. Confrontiamo 'rc' con mqtt.ReasonCode.OK.
    flags e properties sono inclusi per compatibilità.
    """
    if mqtt.ReasonCode.is_failure: # Confronta direttamente l'oggetto ReasonCode
        print(f"Disconnessione inaspettata dal broker! Codice di ritorno: {rc}")
    else:
        print("Disconnesso dal broker MQTT.")

# --- Main Program ---

# Indirizzo del broker Mosquitto. Assicurati che sia accessibile dalla tua macchina.
# Se Mosquitto è in esecuzione sulla stessa macchina, puoi usare "localhost".
# Se Mosquitto è su un'altra macchina, usa il suo indirizzo IP (es. "192.168.1.99").
broker_address = "192.168.1.99"
port = 1883  # Porta standard per MQTT non crittografato

# Genera un ID client unico per evitare conflitti se più client si connettono
client_id = f"PythonClient-{random.randint(0, 1000)}"

print(f"Creazione nuova istanza client con ID: {client_id}")
# Specifica il protocollo MQTTv311 e la versione dell'API dei callback
client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

# Collega le funzioni di callback agli eventi del client
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Poiché il broker Mosquitto è configurato con 'allow_anonymous true',
# non è necessario impostare username e password.
# client.username_pw_set(username, pwd) # Rimuovi o commenta questa riga

try:
    print(f"Connessione al broker {broker_address}:{port}...")
    client.connect(broker_address, port)  # Connessione al broker

    # Avvia il loop in un thread separato. Questo permette al client di
    # gestire le connessioni, sottoscrizioni e messaggi in background.
    client.loop_start()

    # Aspetta un momento per assicurarsi che la connessione e la sottoscrizione siano stabilite
    time.sleep(2)

    print("Pubblicazione del messaggio 'ON' sul topic 'Status'")
    # Pubblica un messaggio con QoS 1 per garantire la consegna
    client.publish("Status", "ON", qos=1)

    # Aspetta un tempo sufficiente per ricevere il messaggio pubblicato
    # (se il client è sottoscritto allo stesso topic) e per eventuali altre interazioni.
    print("In attesa di messaggi per 10 secondi...")
    time.sleep(10)

except Exception as e:
    print(f"Si è verificato un errore: {e}")

finally:
    print("Interruzione del loop del client...")
    client.loop_stop()  # Ferma il loop del client
    print("Disconnessione dal broker...")
    client.disconnect() # Disconnette il client
    print("Script terminato.")
