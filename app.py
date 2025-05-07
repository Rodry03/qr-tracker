from flask import Flask, render_template, redirect, url_for
import sqlite3
import os
import sqlite3

# Crear base de datos y tabla de visitas
def create_db():
    conn = sqlite3.connect('data/visitas.db')  # Asegúrate de que la carpeta 'data' exista
    cursor = conn.cursor()

    # Crear la tabla 'visitas'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

create_db()
app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def home():
    return render_template('index.html')  # Renderiza el archivo index.html

# Ruta para redirigir a un PDF (en este caso, un archivo en Google Drive)
@app.route('/pdf')
def redirect_pdf():
    # Redirige a un enlace de Google Drive (o cualquier otro enlace de un archivo PDF)
    return redirect("https://docs.google.com/spreadsheets/d/1zg8uJw3yE1akzoAIvISN5BKDCjrU6zgLTanvl7g84tI/edit?usp=sharing")

# Ruta para mostrar las estadísticas de visitas
@app.route('/stats')
def stats():
    # Conectar a la base de datos SQLite para obtener las estadísticas
    db_path = 'data/visitas.db'
    if not os.path.exists(db_path):
        return "Base de datos no encontrada", 500
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Consulta para contar las visitas
    cursor.execute("SELECT COUNT(*) FROM visitas")
    visitas_count = cursor.fetchone()[0]
    
    # Consulta para obtener detalles sobre las visitas (si es necesario)
    cursor.execute("SELECT * FROM visitas LIMIT 10")  # Aquí puedes ajustar la consulta
    visitas = cursor.fetchall()
    
    conn.close()

    # Mostrar estadísticas (puedes personalizar este formato)
    stats_html = f"""
    <h1>Estadísticas de Visitas</h1>
    <p>Total de visitas: {visitas_count}</p>
    <h2>Últimas 10 visitas:</h2>
    <ul>
    """
    
    for visita in visitas:
        stats_html += f"<li>{visita}</li>"  # Personaliza cómo mostrar la visita
    
    stats_html += "</ul>"
    
    return stats_html  # Muestra las estadísticas en formato HTML

# Inicia la aplicación
if __name__ == "__main__":
    app.run(debug=True)
