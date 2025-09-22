import sqlite3
from database import DB_NAME
import pytz
from datetime import datetime


def mostrar_tareas(usuario_id=None, es_admin=False):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        if es_admin:
            cursor.execute('''
                SELECT t.id, t.titulo, t.descripcion, t.fecha_creacion, 
                       t.completada, t.trabajador_id, u.username as usuario_nombre,
                       w.nombre as trabajador_nombre
                FROM tareas t
                LEFT JOIN usuarios u ON t.usuario_id = u.id
                LEFT JOIN trabajadores w ON t.trabajador_id = w.id
                ORDER BY t.fecha_creacion DESC;
            ''')
        else:
            cursor.execute('''
                SELECT t.id, t.titulo, t.descripcion, t.fecha_creacion, 
                       t.completada, t.trabajador_id, NULL as usuario_nombre,
                       w.nombre as trabajador_nombre
                FROM tareas t
                LEFT JOIN trabajadores w ON t.trabajador_id = w.id
                WHERE t.usuario_id = ?
                ORDER BY t.fecha_creacion DESC;
            ''', (usuario_id,))
            
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al mostrar tareas: {e}")
        return []
    finally:
        conexion.close()

def marcar_completada(id_tarea, usuario_id=None, es_admin=False):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        # Verificar permisos para usuarios normales
        if not es_admin:
            cursor.execute('SELECT usuario_id FROM tareas WHERE id = ?', (id_tarea,))
            resultado = cursor.fetchone()
            if not resultado or resultado[0] != usuario_id:
                return False
        
        # Cambiar estado
        cursor.execute('''
            UPDATE tareas 
            SET completada = NOT completada 
            WHERE id = ?
        ''', (id_tarea,))
        conexion.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al marcar tarea como completada: {e}")
        return False
    finally:
        conexion.close()

def eliminar_tarea(id_tarea, usuario_id=None, es_admin=False):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        # Solo verificar permisos si NO es admin
        if not es_admin:
            cursor.execute('SELECT usuario_id FROM tareas WHERE id = ?', (id_tarea,))
            resultado = cursor.fetchone()
            if not resultado or resultado[0] != usuario_id:
                return False  # Usuario normal no puede eliminar tareas ajenas
        
        cursor.execute('DELETE FROM tareas WHERE id = ?', (id_tarea,))
        conexion.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar tarea: {e}")
        return False
    finally:
        conexion.close()
        
def obtener_tarea_por_id(id_tarea, usuario_id=None, es_admin=False):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        if es_admin:
            cursor.execute('''
                SELECT t.*, u.username as usuario_nombre
                FROM tareas t
                LEFT JOIN usuarios u ON t.usuario_id = u.id
                WHERE t.id = ?
            ''', (id_tarea,))
        else:
            cursor.execute('''
                SELECT t.*, NULL as usuario_nombre
                FROM tareas t
                WHERE t.id = ? AND t.usuario_id = ?
            ''', (id_tarea, usuario_id))
            
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error al obtener tarea: {e}")
        return None
    finally:
        conexion.close()
        
def actualizar_tarea(id_tarea, nuevo_titulo, nueva_descripcion, usuario_id=None, es_admin=False):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        # Verificar permisos para usuarios normales
        if not es_admin:
            cursor.execute('SELECT usuario_id FROM tareas WHERE id = ?', (id_tarea,))
            resultado = cursor.fetchone()
            if not resultado or resultado[0] != usuario_id:
                return False
        
        cursor.execute('''
            UPDATE tareas 
            SET titulo = ?, descripcion = ?
            WHERE id = ?
        ''', (nuevo_titulo, nueva_descripcion, id_tarea))
        conexion.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar tarea: {e}")
        return False
    finally:
        conexion.close()

# Las funciones de trabajadores permanecen igual
def agregar_trabajador(nombre, cargo):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO trabajadores (nombre, cargo) VALUES (?, ?)', 
                     (nombre, cargo))
        conexion.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al agregar trabajador: {e}")
        return False
    finally:
        conexion.close()

def obtener_trabajadores():
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM trabajadores ORDER BY nombre')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener trabajadores: {e}")
        return []
    finally:
        conexion.close()

def eliminar_trabajador(id_trabajador):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM trabajadores WHERE id = ?', (id_trabajador,))
        conexion.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar trabajador: {e}")
        return False
    finally:
        conexion.close()

def agregar_tarea(titulo, descripcion, trabajador_id=None, usuario_id=None):
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        lima_tz = pytz.timezone('America/Lima')
        fecha_actual = datetime.now(lima_tz)
        
        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, trabajador_id, usuario_id, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, descripcion, trabajador_id, usuario_id, fecha_actual.strftime('%Y-%m-%d %H:%M:%S')))
        
        conexion.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al agregar tarea: {e}")
        return False
    finally:
        conexion.close()