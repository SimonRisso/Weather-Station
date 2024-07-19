import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish
import time
from class_firebase_database import FirebaseDB
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de Firebase
path = os.getenv('FIREBASE_CREDENTIALS_PATH')
url = os.getenv('FIREBASE_DATABASE_URL')
fb_db = FirebaseDB(path, url)

broker_address = "broker.emqx.io"
topic = "test/broker"

# Función para manejar la conexión
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
        client.subscribe(topic)
    else:
        print("Conexión fallida, código de resultado: ", str(rc))

# Función para manejar los mensajes recibidos
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Mensaje recibido del tópico {msg.topic}: {message}")

    # Obtener la fecha y hora actual
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Almacenar el mensaje en Firebase con fecha y hora, usando timestamp como clave
    data = {
        'message': message,
        'timestamp': timestamp
    }
    fb_db.write_record(f"/mqtt/messages/{timestamp}", data)

# Función para publicar datos en el tópico
def publish_data():
    pin = 3
    while True:
        mqtt_publish.single("test/broker", str(pin), hostname=broker_address)
        time.sleep(1)

# Función para suscribirse al tópico
def subscribe_to_topic():
    # Crear una instancia del cliente MQTT
    client = mqtt.Client()

    # Asignar las funciones de callback
    client.on_connect = on_connect
    client.on_message = on_message

    # Conectar al broker
    client.connect(broker_address, 1883, 60)

    # Mantener el cliente en ejecución
    client.loop_start()

    try:
        while True:
            pass  # Mantener el programa en ejecución para recibir mensajes
    except KeyboardInterrupt:
        print("Desconectando...")
        client.loop_stop()
        client.disconnect()

# Ejecutar la publicación y suscripción en hilos separados
if __name__ == "__main__":
    import threading

    # Hilo para la publicación de datos
    publish_thread = threading.Thread(target=publish_data)
    publish_thread.start()

    # Hilo para la suscripción al tópico
    subscribe_thread = threading.Thread(target=subscribe_to_topic)
    subscribe_thread.start()
