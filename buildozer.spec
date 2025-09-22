[app]

# Título de tu aplicación - se mostrará en el dispositivo
title = Gestor de Tareas

# Nombre del paquete (debe ser único en Google Play)
package.name = gestortareas

# Dominio del paquete (formato invertido del dominio)
package.domain = com.nelsontareas

# Directorio del código fuente
source.dir = .

# Archivos a incluir (asegúrate de incluir todos los recursos necesarios)
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,db,json
source.include_patterns = resources/*
source.exclude_dirs = tests, bin, venv, .venv

# Archivos específicos a incluir
source.include_files = README.md,LICENSE,tasksBD.db

# Versión de la aplicación (importante para actualizaciones)
version = 1.0.0

# Si prefieres usar version.regex, comenta la línea version arriba y descomenta estas:
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# Requerimientos (todos los paquetes necesarios para la app)
requirements = python3,
    kivy==2.2.1,
    pillow,
    sqlite3,
    pytz

# Orientación (portrait para móviles)
orientation = portrait

# Pantalla completa
fullscreen = 0

# Permisos para Android (solo los necesarios)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Configuración de Android
# Android SDK configuration
android.api = 30
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# SDK path configuration
android.sdk_path = ~/Android/Sdk
android.ndk_path = ~/Android/Sdk/ndk/25.2.9519653
android.archs = arm64-v8a, armeabi-v7a

# Configuración de compilación
android.accept_sdk_license = True
android.allow_backup = True
android.debug_artifact = apk

# Iconos y branding
android.presplash_color = #FFFFFF
android.icon.filename = %(source.dir)s/resources/icon.png
android.presplash.filename = %(source.dir)s/resources/presplash.png
android.adaptive_icon.background.filename = %(source.dir)s/resources/icon_background.png
android.adaptive_icon.foreground.filename = %(source.dir)s/resources/icon_foreground.png

# Optimizaciones
android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.7.0
android.add_packaging_options = doNotStrip "*/*/libsqlite3.so"

# Configuración de buildozer
[buildozer]
log_level = 2
warn_on_root = 1

#############################################
# Configuraciones avanzadas (puedes dejarlas así)
#############################################

# (str) Presplash background color
#android.presplash_color = #FFFFFF

# (str) Adaptive icon foreground
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png

# (bool) Skip byte compile for .py files
#android.no-byte-compile-python = False

# (list) Gradle dependencies
#android.gradle_dependencies =

# (bool) Enable AndroidX support
#android.enable_androidx = False

# (list) Java classes to add as activities
#android.add_activities =

# (list) Gradle repositories to add
#android.gradle_repositories =

# (list) Packaging options to add
#android.add_packaging_options =