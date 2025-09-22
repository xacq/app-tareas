# Script para compilar en Google Colab
# Guarda este código y súbelo a Colab junto con tu proyecto

import os
from google.colab import drive

# Montar Google Drive
drive.mount('/content/drive')

# Navegar a tu carpeta de proyecto
project_path = '/content/drive/MyDrive/tu_proyecto'
os.chdir(project_path)

# Instalar Buildozer
!pip install buildozer

# Inicializar Buildozer si no existe el archivo spec
if not os.path.exists('buildozer.spec'):
    !buildozer init

# Compilar para Android
!buildozer -v android debug

# El APK estará en la carpeta bin/