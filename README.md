# Gestor de Tareas con Kivy

Una aplicación de gestión de tareas multiplataforma desarrollada con Python y Kivy, con soporte para múltiples usuarios, sistema de autenticación y base de datos SQLite.

## Características

- ✅ Sistema de autenticación de usuarios (normal/admin)
- 📝 Gestión completa de tareas (CRUD)
- 👥 Sistema de trabajadores asignables
- 📱 Interfaz gráfica adaptativa
- 🔒 Almacenamiento seguro de contraseñas
- 📅 Seguimiento de fechas de creación
- 🌍 Soporte para zona horaria local

## Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual de Python (recomendado)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/xacq/app-tareas.git
cd app-tareas
```

2. Crear y activar un entorno virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install kivy==2.2.1
pip install pillow
pip install pytz
```

## Ejecución

1. Activar el entorno virtual (si no está activado):
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. Ejecutar la aplicación:
```bash
python main.py
```

## Estructura del Proyecto

```
app-tareas/
├── main.py              # Archivo principal de la aplicación
├── auth.py             # Sistema de autenticación
├── database.py         # Gestión de base de datos
├── tasks.py            # Lógica de tareas
├── *.kv               # Archivos de diseño Kivy
├── tasksBD.db         # Base de datos SQLite
└── crear_superusuario.py  # Utilidad para crear admin
```

## Compilación para Android

### Requisitos

- Linux/WSL
- Java Development Kit (JDK)
- Android SDK
- Buildozer

### Pasos para compilar

1. Instalar dependencias (en Ubuntu/WSL):
```bash
sudo apt update
sudo apt install -y python3 python3-pip git wget unzip openjdk-17-jdk
sudo apt install -y python3-dev build-essential libssl-dev libffi-dev libltdl-dev libtool pkg-config zlib1g-dev cmake
```

2. Instalar Buildozer:
```bash
pip install buildozer
```

3. Preparar el entorno de Android:
   - Buildozer descargará automáticamente el SDK y el NDK en la carpeta `.buildozer/android` la primera vez que ejecutes un comando de compilación.
   - Si ya tienes una instalación existente, exporta las variables de entorno antes de compilar para que Buildozer las detecte:
     ```bash
     export ANDROIDSDK_HOME="/ruta/a/Android/Sdk"
     export ANDROIDNDK_HOME="$ANDROIDSDK_HOME/ndk/25.2.9519653"
     ```

4. Limpiar y compilar el APK:
```bash
buildozer android clean
buildozer android debug
```

El archivo APK se generará en la carpeta `bin/`.

## Uso

1. **Inicio de Sesión**
   - Usar credenciales existentes o crear nueva cuenta
   - Los administradores tienen acceso a funciones adicionales

2. **Gestión de Tareas**
   - Crear nuevas tareas
   - Asignar tareas a trabajadores
   - Marcar tareas como completadas
   - Editar o eliminar tareas existentes

3. **Panel de Administración**
   - Gestionar usuarios
   - Ver todas las tareas
   - Administrar trabajadores

## Seguridad

- Contraseñas almacenadas con hash SHA-256
- Validación de permisos por rol
- Protección contra SQL injection
- Manejo seguro de sesiones

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu función (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## Contacto

Xavier Carrera - [@xacq](https://github.com/xacq)

Link del Proyecto: [https://github.com/xacq/app-tareas](https://github.com/xacq/app-tareas)