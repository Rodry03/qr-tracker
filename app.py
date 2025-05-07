from flask import Flask, render_template, redirect
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'tmp/visitas.db'

def create_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            user_agent TEXT,
            ruta TEXT,
            referer TEXT
        )
    ''')
    conn.commit()
    conn.close()

def registrar_visita(ruta):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO visitas (timestamp, ip, user_agent, ruta, referer)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (
            datetime.utcnow().isoformat(),
            request.remote_addr,
            request.headers.get('User-Agent'),
            ruta,
            request.headers.get('Referer')
        )
    )
    conn.commit()
    conn.close()

@app.route('/')
def index():
    registrar_visita('/')
    return render_template('index.html')

@app.route('/pdf')
def redirect_pdf():
    registrar_visita('/pdf')
    return redirect("https://siemprefiel.es/")  # Aquí va la web a la que quieres redirigir


@app.route('/stats')
@app.route('/stats')
def stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, ip, user_agent, ruta, referer FROM visitas ORDER BY timestamp DESC")
    visitas = cursor.fetchall()
    conn.close()
    return render_template('stats.html', visitas=visitas)

if __name__ == "__main__":
    app.run(debug=True)
