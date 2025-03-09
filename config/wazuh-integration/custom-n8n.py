#!/usr/bin/env python3

import sys
import requests
import json

# Leer argumentos pasados por Wazuh
alert_file = sys.argv[1]
hook_url = sys.argv[2]  # Ahora se pasa directamente desde ossec.conf

# Leer contenido del archivo de alerta
try:
    with open(alert_file, "r") as f:
        alert_json = json.load(f)
except Exception as e:
    print(f"Error al leer el archivo de alerta: {e}")
    sys.exit(1)

# Extraer datos de la alerta
alert_level = alert_json.get("rule", {}).get("level", "N/A")
alert_description = alert_json.get("rule", {}).get("description", "Sin descripción")
agent_name = alert_json.get("agent", {}).get("name", "Desconocido")

# Construir el payload para n8n
payload = {
    "title": f"Wazuh Alert - Nivel {alert_level}",
    "description": alert_description,
    "agent": agent_name,
}

# Enviar la alerta al webhook de n8n
try:
    headers = {"Content-Type": "application/json"}
    response = requests.post(hook_url, json=payload, headers=headers)
    response.raise_for_status()
    print(f"✅ Alerta enviada con éxito: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"❌ Error enviando alerta: {e}")
    sys.exit(1)

sys.exit(0)
