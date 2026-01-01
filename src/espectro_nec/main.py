import ttkbootstrap as ttk
from .app import EspectroSismicoApp

def main():
    root = ttk.Window(themename="litera")
    app = EspectroSismicoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()