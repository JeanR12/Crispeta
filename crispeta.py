
import os
import json
import hashlib
import logging
import smtplib
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import time

# Aqui va la configuracion del loggin 
logging.basicConfig(filename='crispeta.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Esta función sirve para enviar notificaciones por correo electrónico
def send_email_notification(subject, body, to_email):
    from_email = "su_email@example.com"
    password = "su_email_password"

    msg = MIMEText(body)
    msg["Subjeto"] = subject
    msg["De"] = from_email
    msg["Para"] = to_email

    with smtplib.SMTP_SSL("smtp.example.com", 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

# Aqui se genera una clave de cifrado
def generate_key():
    return Fernet.generate_key()

# Aqui se guarda la clave de cifrado en un archivo
def save_key(key, file_name="secret.key"):
    with open(file_name, "wb") as key_file:
        key_file.write(key)

# Cargar la clave de cifrado desde un archivo
def load_key(file_name="secret.key"):
    return open(file_name, "rb").read()

# Cifrar un archivo
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted_data)
    os.remove(file_path)
    logging.info(f"El Archivo ya esta cifrado mi papito bello: {file_path}")

# Descifrar un archivo
def decrypt_file(file_path, key, password):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path[:-4], "wb") as file:
        file.write(decrypted_data)
    os.remove(file_path)
    logging.info(f"Archivo descifrado mi apito, ojo: {file_path}")

# Función para generar y verificar la contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password_hash, provided_password):
    return stored_password_hash == hash_password(provided_password)

# Configuración inicial
def initial_setup():
    key = generate_key()
    save_key(key)
    password = input("Papi asigne una contraseña viejo: ")
    email = input("Meta ese hijuemadre email ps pa' avisarle cualquier cosa precios@: ")
    config = {
        "release_schedule": [],
        "password_hash": hash_password(password),
        "notificacion_email": email
    }
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
    logging.info("ahhh no pa configuración inicial completada, en pocas palabras pri, yastuvo")

# Añadir un archivo a la programación de liberación
def add_file_to_schedule(file_path, release_datetime):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    config["release_schedule"].append({
        "file_path": file_path + ".enc",
        "release_datetime": release_datetime
    })
    
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
    
    key = load_key()
    encrypt_file(file_path, key)
    logging.info(f"El archivo {file_path} fue cifrado y programado para liberación el {release_datetime}")

# Función principal para manejar el calendario de liberación
def release_files():
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
        
        release_schedule = config["release_schedule"]
        updated_schedule = []
        
        for item in release_schedule:
            if item["release_datetime"] <= current_time:
                key = load_key()
                password = input(f"Meta la contraseña para liberarlo {item['file_path']}: ")
                if check_password(config["password_hash"], password):
                    decrypt_file(item["file_path"], key, password)
                    logging.info(f"El archivo {item['file_path']} ya puede ser manoseado xd")
                    send_email_notification(
                        "Archivo Libre como las gallinas",
                        f"El archivo {item['file_path']} ha sido liberado mi apito.",
                        config["notification_email"]
                    )
                else:
                    logging.warning(f"Uy viejo, usted quien es, esa no es la contrasela pa {item['file_path']}")
                    updated_schedule.append(item)
            else:
                updated_schedule.append(item)
        
        config["release_schedule"] = updated_schedule
        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        
        time.sleep(60)

if __name__ == "__main__":
    if not os.path.exists("config.json"):
        initial_setup()
    
    while True:
        action = input("Elija una opcio pa: [1] Agregar un archivo a la programacion [2] Iniciar un proceso: ")
        if action == "1":
            file_path = input("Meta la ruta del archivo menor: ")
            release_datetime = input("Meta el dia y la hora mijo (YYYY-MM-DD HH:MM): ")
            add_file_to_schedule(file_path, release_datetime)
        elif action == "2":
            release_files()
        else:
            print("Accion invalida menor. Elija la opcion 1 o 2 menor")
