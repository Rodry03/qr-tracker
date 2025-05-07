from flask import Flask, request, redirect, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

PDF_URL = "https://docs.google.com/spreadsheets/d/1zg8uJw3yE1akzoAIvISN5BKDCjrU6zgLTanvl7g84tI/edit?usp=sharing"  # ← Cambia este enlace

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

@app.route("/stats")
def mostrar_stats():
    conn = sqlite3.connect("visitas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, ip, user_agent FROM visitas ORDER BY id DESC")
    visitas = cursor.fetchall()
    conn.close()

    html_template = """
    <h1>Visitas registradas</h1>
    <table border="1" cellpadding="5">
        <tr><th>Fecha</th><th>IP</th><th>User Agent</th></tr>
        {% for v in visitas %}
        <tr>
            <td>{{ v[0] }}</td>
            <td>{{ v[1] }}</td>
            <td>{{ v[2] }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html_template, visitas=visitas)
