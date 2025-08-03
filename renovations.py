"""
Script para la gestión y notificación de renovaciones de licencias de software.

Este script se conecta a una hoja de cálculo de Google Sheets que contiene información sobre licencias de software, fechas de renovación, correos electrónicos y montos a pagar. Verifica si alguna licencia está próxima a vencer (según un número configurable de días de anticipación) y, en caso afirmativo, envía un correo electrónico de notificación al responsable utilizando una plantilla HTML personalizada.

Funciones principales:
- cargar_plantilla_html: Carga y personaliza la plantilla de correo electrónico.
- cargar_datos_google_sheets: Obtiene los datos de la hoja de cálculo de Google Sheets.
- enviar_correo: Envía un correo electrónico de notificación.
- verificar_renovaciones: Procesa los datos y gestiona el envío de notificaciones.

Requiere un archivo de credenciales para Google API y variables de entorno para la configuración del correo electrónico.
"""
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os
from string import Template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.multipart import MIMEMultipart

# Configuración
DIAS_ANTICIPACION = 7
EMAIL_ORIGEN = os.getenv("EMAIL_ORIGEN")
EMAIL_CLAVE = os.getenv("EMAIL_CLAVE")  # Contraseña de app de Gmail
EMAIL_SERVIDOR = "smtp.gmail.com"
EMAIL_PUERTO = 465
# Cambiar a lista de nombres de hojas
SPREADSHEET_NOMBRES = ["Licencias"]  # Puedes agregar más nombres aquí
CREDENCIALES_JSON = "credenciales.json"    # Nombre del archivo de credenciales




def cargar_plantilla_html(software, fecha, monto):
    """
    Carga y personaliza la plantilla HTML para el correo electrónico de notificación.

    Args:
        software (str): Nombre del software a renovar.
        fecha (str): Fecha de renovación.
        monto (str): Monto a pagar por la renovación.

    Returns:
        str: Contenido HTML del correo con los datos personalizados.
    """
    with open("plantilla_email.html", "r", encoding="utf-8") as file:
        contenido = Template(file.read())
        return contenido.safe_substitute(software=software, fecha=fecha, monto=monto)


def cargar_datos_google_sheets(sheet_names):
    """
    Obtiene los datos de varias hojas de cálculo de Google Sheets.
    Args:
        sheet_names (list): Lista de nombres de hojas a procesar.
    Returns:
        list: Lista de diccionarios con los datos de cada fila de todas las hojas.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, scope)
    client = gspread.authorize(creds)
    all_data = []
    for name in sheet_names:
        try:
            sheet = client.open(name).sheet1
            data = sheet.get_all_records()
            all_data.extend(data)
        except Exception as e:
            print(f"Error accediendo a la hoja '{name}': {e}")
    return all_data



def enviar_correo(destinatario, software, fecha, monto):
    """
    Envía un correo electrónico de notificación de renovación de licencia.

    Args:
        destinatario (str): Correo electrónico del destinatario.
        software (str): Nombre del software a renovar.
        fecha (str): Fecha de renovación.
        monto (str): Monto a pagar por la renovación.
    """
    html_body = cargar_plantilla_html(software, fecha, monto)

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = f"📌 Renovación pendiente: {software}"
    mensaje["From"] = EMAIL_ORIGEN
    mensaje["To"] = destinatario

    mensaje.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL(EMAIL_SERVIDOR, EMAIL_PUERTO) as server:
            server.login(EMAIL_ORIGEN, EMAIL_CLAVE)
            server.send_message(mensaje)
        print(f"Correo enviado a {destinatario} por {software}")
    except Exception as e:
        print(f"Error enviando correo a {destinatario}: {e}")


def verificar_renovaciones():
    """
    Verifica las renovaciones próximas y envía notificaciones por correo electrónico si corresponde.
    """
    hoy = datetime.today().date()
    datos = cargar_datos_google_sheets(SPREADSHEET_NOMBRES)
    for fila in datos:
        try:
            fecha_renovacion = datetime.strptime(fila["Fecha de renovación"], "%Y-%m-%d").date()
            dias_restantes = (fecha_renovacion - hoy).days
            if dias_restantes in [1, 7]:
                enviar_correo(
                    fila["Correo"],
                    fila["Nombre del software"],
                    fecha_renovacion,
                    fila["Monto a pagar"]
                )
        except Exception as e:
            print(f"Error procesando fila: {e}")

if __name__ == "__main__":
    verificar_renovaciones()
