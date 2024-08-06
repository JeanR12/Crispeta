
# Crispeta

## Descripción

Crispeta es una herramienta avanzada para cifrar archivos y programar su liberación en horas y días específicos, con acceso protegido por una contraseña. Incluye funcionalidades criptográficas y notificaciones por correo electrónico.

## Requisitos

- Python 3.x
- Librerías Python: `requests`, `cryptography` (detalladas en `requirements.txt`)

## Instalación

Instala las librerías necesarias usando pip:
```
pip install -r requirements.txt
```

## Configuración

El archivo `config.json` se utiliza para configurar los parámetros del script.

## Uso

Para ejecutar el script, abre una terminal, navega al directorio donde se encuentra el script y ejecuta:
```
python crispeta.py
```

Los resultados se guardarán en el archivo `crispeta.log`.

## Funcionalidades

- **Cifrado de archivos**: Cifra archivos y los programa para su liberación.
- **Descifrado de archivos**: Descifra archivos en horarios programados.
- **Notificaciones por correo electrónico**: Envía notificaciones cuando los archivos son liberados.
- **Logging detallado**: Registra todas las operaciones en un archivo de log.

## Contribuciones

Si deseas contribuir a este proyecto, haz un fork y envía un pull request.

