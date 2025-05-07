from flask import Flask, render_template, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/tmp/visitas.db'  # Carpeta con permisos de escritura en Render

def create_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ruta TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

create_db()

@app.route('/')
def home():
    # Insertar registro de visita a la home
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visitas (ruta) VALUES (?)", ('/main',))
    conn.commit()
    conn.close()

    return render_template('index.html')

@app.route('/pdf')
def redirect_pdf():
    # Insertar registro de visita
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visitas (ruta) VALUES (?)", ('/web',))
    conn.commit()
    conn.close()
    
    return redirect("https://drive.google.com/file/d/TU_ID/view")

@app.route('/stats')
def stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visitas")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT * FROM visitas ORDER BY timestamp DESC LIMIT 10")
    visitas = cursor.fetchall()
    conn.close()

    stats_html = f"<h1>Total visitas: {total}</h1><ul>"
    for v in visitas:
        stats_html += f"<li>{v}</li>"
    stats_html += "</ul>"

    return stats_html

if __name__ == "__main__":
    app.run(debug=True)
