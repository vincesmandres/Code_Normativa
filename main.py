import tkinter as tk
from app import EspectroSismicoApp

def main():
    root = tk.Tk()
    app = EspectroSismicoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()