# 🛠 Automatización de Renovación de Licencias

Este proyecto automatiza el envío de recordatorios de renovación de licencias de software, leyendo datos desde Google Sheets y notificando a los responsables mediante correo electrónico.

---

## 📌 Funcionalidades

- 📅 Verifica fechas de renovación desde una hoja de cálculo compartida.
- 📬 Envía correos personalizados con HTML a los responsables de cada software.
- 🔄 Ejecutado automáticamente todos los días a las 8:00 a.m. Colombia vía GitHub Actions.
- 📅 Generar una alerta de vencimiento 7 días antes y otra 1 día antes de la fecha límite a la persona responsable (Correo registrado).
- 🔐 Manejo seguro de credenciales con GitHub Secrets.

---

## 📁 Estructura del proyecto

```
SHEETSTEST/
├── renovations.py              # Script principal
├── plantilla_email.html         # Plantilla de correo en HTML
├── requirements.txt             # Dependencias
└── .github/
    └── workflows/
        └── renovaciones.yml     # GitHub Actions
```

---

## 🚀 Configuración

1. Crea una cuenta de servicio en Google Cloud y activa la API de Sheets.
2. Descarga el archivo `credenciales.json` y guárdalo como Secret:
   - `CREDENTIALS_JSON`: contenido del archivo en formato minificado (una línea)
3. Crea dos secrets adicionales:
   - `EMAIL_ORIGEN`: tu correo Gmail
   - `EMAIL_CLAVE`: contraseña de aplicación de Gmail (no la normal)
4. Comparte tu hoja de cálculo con la cuenta de servicio.

---

## 📋 Variables esperadas en Google Sheets

| Nombre del software | Fecha de renovación | Monto a pagar | Correo |
|---------------------|---------------------|----------------|--------|
| Asana               | 2025-08-15          | 75.00          | alguien@example.com |

- La hoja debe tener este encabezado.
- La fecha debe estar en formato `YYYY-MM-DD`.

---

## 📩 Ejemplo del correo HTML

Se usa una plantilla simple, con colores suaves y diseño adaptado a clientes de correo. El contenido incluye nombre del software, monto y fecha.

---

## 🧠 Escalabilidad y mejoras

- Puedes integrar con Slack mediante webhooks.
- Escalar a múltiples hojas o separar por equipos.
- Usar bases de datos como alternativa a Google Sheets en proyectos más grandes.

---

## 👨‍💻 Autor

Daniel Fuentes  
[https://github.com/danielfard](https://github.com/danielfard)
