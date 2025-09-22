from auth import crear_usuario
from getpass import getpass  # Para ocultar la contraseña al escribir

def crear_superusuario():
    print("\n=== CREAR SUPERUSUARIO ===")
    usuario = input("Nombre de usuario admin: ").strip()
    contraseña = getpass("Contraseña: ").strip()
    confirmar = getpass("Confirmar contraseña: ").strip()

    if contraseña != confirmar:
        print("\n❌ Las contraseñas no coinciden")
        return

    if crear_usuario(usuario, contraseña, rol="admin"):
        print(f"\n✅ Superusuario '{usuario}' creado exitosamente!")
    else:
        print("\n❌ Error al crear el superusuario (¿ya existe?)")

if __name__ == "__main__":
    crear_superusuario()