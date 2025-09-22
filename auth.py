import sqlite3
import hashlib
from database import DB_NAME

def crear_usuario(username, password, rol='normal'):
    try:
        if not username or not password:
            print("Nombre de usuario y contraseña son requeridos")
            return False
            
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        if usuario_existe(username):
            print(f"El usuario '{username}' ya existe")
            return False
            
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)', 
                      (username, hashed_pw, rol))
        
        conexion.commit()
        print(f"Usuario '{username}' creado exitosamente")
        return True
    except sqlite3.Error as e:
        print(f"Error al crear usuario '{username}': {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def obtener_rol_usuario(usuario_id):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('SELECT rol FROM usuarios WHERE id = ?', (usuario_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 'normal'
    except sqlite3.Error as e:
        print(f"Error al obtener rol para usuario {usuario_id}: {e}")
        return 'normal'
    finally:
        if conexion:
            conexion.close()

def verificar_usuario(username, password):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('SELECT id, rol FROM usuarios WHERE username = ? AND password = ?', 
                      (username, hashed_pw))
        return cursor.fetchone()  # Devuelve (id, rol) o None
    except sqlite3.Error as e:
        print(f"Error al verificar usuario '{username}': {e}")
        return None
    finally:
        if conexion:
            conexion.close()

def usuario_existe(username):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('SELECT 1 FROM usuarios WHERE username = ?', (username,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Error al verificar existencia de usuario '{username}': {e}")
        return False
    finally:
        if conexion:
            conexion.close()