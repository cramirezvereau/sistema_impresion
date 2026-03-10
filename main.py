# main.py
import customtkinter as ctk
from ui import PrinterAppUI

def main():
    root = ctk.CTk()
    app = PrinterAppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()