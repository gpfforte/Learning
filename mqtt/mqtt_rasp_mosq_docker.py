import paho.mqtt.client as mqtt  # Importa il client Paho MQTT
import time
import random # Per generare un ID client unico

# --- Callback Functions ---

def on_connect(client, userdata, flags, rc):
    """
    Callback che viene chiamato quando il client si connette al broker.
    rc (return code) indica il risultato della connessione:
    0: Connessione riuscita
    1: Protocollo non corretto
    2: ID client non valido
    3: Server non disponibile
    4: Username/password non validi (non applicabile se allow_anonymous è true)
    5: Non autorizzato
    """
    if rc == 0:
        print("Connesso al broker MQTT! (Codice di ritorno: {})".format(rc))
        # Sottoscrivi al topic qui. Questo assicura che la sottoscrizione
        # venga ristabilita se la connessione cade e si riconnette.
        client.subscribe("Status", qos=1) # Sottoscrivo con QoS 1
        print("Sottoscritto al topic 'Status'")
    else:
        print("Fallita la connessione al broker! Codice di ritorno: {}".format(rc))

def on_message(client, userdata, msg):
    """
    Callback che viene chiamato quando un messaggio viene ricevuto dal broker.
    """
    print(f"Messaggio ricevuto: '{msg.payload.decode('utf-8')}'")
    print(f"Topic: '{msg.topic}'")
    print(f"QoS: {msg.qos}")
    print(f"Flag Retain: {msg.retain}")

def on_publish(client, userdata, mid):
    """
    Callback che viene chiamato quando un messaggio pubblicato è stato confermato dal broker.
    mid (message ID) è l'ID del messaggio pubblicato.
    """
    print(f"Messaggio pubblicato con ID: {mid}")

def on_disconnect(client, userdata, rc):
    """
    Callback che viene chiamato quando il client si disconnette dal broker.
    """
    if rc != 0:
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
client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)

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