from flask import Flask, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

PDF_URL = "https://docs.google.com/spreadsheets/d/1zg8uJw3yE1akzoAIvISN5BKDCjrU6zgLTanvl7g84tI/edit?usp=sharing"  # <-- CAMBIA ESTO

@app.route("/pdf")
def redirigir_pdf():
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "unknown")
    timestamp = datetime.utcnow().isoformat()

    try:
        conn = sqlite3.connect("visitas.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS visitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_agent TEXT,
                ip TEXT
            )
        """)
        conn.execute(
            "INSERT INTO visitas (timestamp, user_agent, ip) VALUES (?, ?, ?)",
            (timestamp, user_agent, ip)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error guardando visita:", e)

    return redirect(PDF_URL, code=302)
