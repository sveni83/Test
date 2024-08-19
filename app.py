from flask import Flask, request, jsonify
import sqlite3
import random
import speech_recognition as sr
import pyttsx3
from datetime import datetime

app = Flask(__name__)

# Initialisiere die Spracherkennungs- und Synthesemodule
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# SQLite Datenbankverbindung
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Sprachsteuerung - Befehl ausführen
def execute_voice_command(command):
    if command == "status":
        return "System is running smoothly."
    elif command == "time":
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    else:
        return "Unknown command."

# Flask-API Endpunkt für Sprachbefehle
@app.route('/api/v1/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')

    response = execute_voice_command(command)
    
    # Optional: Antwort mit Sprachausgabe
    engine.say(response)
    engine.runAndWait()

    return jsonify({"response": response})

# Flask-API Endpunkt für den Systemstatus
@app.route('/api/v1/status', methods=['GET'])
def get_status():
    status = {
        "system": "online",
        "uptime": "48 hours",
        "temperature": "36.5C",
        "database": "connected" if check_database_connection() else "disconnected"
    }
    
    return jsonify(status)

# Überprüfe die Datenbankverbindung
def check_database_connection():
    try:
        conn = get_db_connection()
        conn.execute('SELECT 1')
        conn.close()
        return True
    except sqlite3.Error:
        return False

# Beispiel für die Integration eines Drittanbieter-APIs (z.B. für Wetterdaten)
@app.route('/api/v1/weather', methods=['GET'])
def get_weather():
    # Hier könntest du eine echte Wetter-API ansprechen
    fake_weather_data = {
        "location": "Berlin",
        "temperature": f"{random.randint(-5, 30)}C",
        "condition": "Cloudy"
    }
    
    return jsonify(fake_weather_data)

if __name__ == '__main__':
    # Datenbank initialisieren (wenn nicht vorhanden)
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.close()

    app.run(debug=True, host='0.0.0.0', port=5000)
