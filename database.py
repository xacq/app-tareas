import sqlite3
import os

DB_NAME = 'tasksBD.db'

def crear_tabla():
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA journal_mode = WAL")
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                fecha_registro TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                rol TEXT DEFAULT 'normal'
            )
        ''')
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trabajadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cargo TEXT
            )
        ''')
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_creacion TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                completada BOOLEAN DEFAULT 0,
                trabajador_id INTEGER,
                usuario_id INTEGER,
                FOREIGN KEY (trabajador_id) REFERENCES trabajadores(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        conexion.commit()
    except Exception as e:
        print(f"Error al crear tabla: {e}")
        raise  # Esto ayudará a ver el error completo
    finally:
        if conexion:
            conexion.close()

def migrar_tabla_tareas():
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        cursor.execute("PRAGMA table_info(tareas)")
        columnas = [col[1] for col in cursor.fetchall()]
        
        if 'trabajador_id' not in columnas:
            cursor.execute('''
                ALTER TABLE tareas
                ADD COLUMN trabajador_id INTEGER
                REFERENCES trabajadores(id)
            ''')
        
        if 'usuario_id' not in columnas:
            cursor.execute('''
                ALTER TABLE tareas
                ADD COLUMN usuario_id INTEGER
                REFERENCES usuarios(id)
            ''')
        
        conexion.commit()
    except Exception as e:
        print(f"Error en migración: {e}")
    finally:
        if conexion:
            conexion.close()