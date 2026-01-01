import os
import subprocess
import sys


def _has_runtime_deps():
    try:
        import numpy  # noqa: F401
        import matplotlib  # noqa: F401
        import pandas  # noqa: F401
        import openpyxl  # noqa: F401
        import reportlab  # noqa: F401
        import ttkbootstrap  # noqa: F401
        return True
    except (ImportError, ModuleNotFoundError):
        return False


def _install_deps():
    root = os.path.dirname(os.path.abspath(__file__))
    requirements = os.path.join(root, "requirements.txt")
    if not os.path.exists(requirements):
        print(f"Error: No se encontró el archivo de requisitos en: {requirements}")
        return 1
    cmd = [sys.executable, "-m", "pip", "install", "-r", requirements]
    return subprocess.call(cmd)


def main():
    if sys.version_info < (3, 10):
        print("Python 3.9 o menor no es compatible.")
        print("Instala Python 3.10, 3.11 o 3.12 y ejecuta: py -3.11 .\\run_app.py")
        sys.exit(1)

    if sys.version_info >= (3, 13):
        print("Python 3.13+ no es compatible con wheels precompiladas de numpy/matplotlib.")
        print("Instala Python 3.10, 3.11 o 3.12 y ejecuta: py -3.11 .\\run_app.py")
        sys.exit(1)
    # Asegurar que 'src' esté en el path para encontrar 'espectro_nec'
    root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(root, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    if not _has_runtime_deps():
        print("Installing dependencies from requirements.txt...")
        rc = _install_deps()
        if rc != 0:
            print("Dependency install failed. Run: python -m pip install -r requirements.txt")
            sys.exit(rc)
        
        print("Dependencies installed. Restarting application...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    try:
        from espectro_nec.main import main as app_main
    except ImportError as e:
        print(f"Error crítico: No se pudo importar la aplicación.\nAsegúrate de que la carpeta 'espectro_nec' exista en {src_path}.\nDetalle: {e}")
        sys.exit(1)

    app_main()


if __name__ == "__main__":
    main()
