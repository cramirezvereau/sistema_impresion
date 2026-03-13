# printer.py
import os
import time
import win32print
import win32ui
from PIL import Image, ImageWin

class PrinterManager:
    def __init__(self):
        self.selected_printer = None
        self.printer_status = "● No verificado"
        self.status_color = ("gray50", "gray60")
    
    def load_printers(self):
        """Buscar y seleccionar automáticamente la EPSON TM-T20II"""
        try:
            printers = [printer[2] for printer in win32print.EnumPrinters(2)]
            print("Impresoras encontradas:", printers)
            target = None
            for p in printers:
                name = p.upper()
                if "EPSON TM-T20II" in name or "TM-T20" in name:
                    target = p
                    break
            if target:
                print("✔ EPSON encontrada y seleccionada:", target)
                self.selected_printer = target
            else:
                print("✗ No se encontró EPSON TM-T20II.")
                self.selected_printer = None
            return self.selected_printer
        except Exception as e:
            print("Error al cargar impresoras:", e)
            return None
    
    def verify_printer(self, printer_name=None):
        """Verificar estado de la impresora"""
        printer_name = printer_name or self.selected_printer
        if not printer_name:
            return False, "No hay impresora seleccionada", ("gray50", "gray60")
        try:
            handle = win32print.OpenPrinter(printer_name)
            info = win32print.GetPrinter(handle, 2)
            win32print.ClosePrinter(handle)
            if info.get("Status", 0) == 0:
                self.printer_status = "● Impresora conectada y lista"
                self.status_color = ("#27ae60", "#2ecc71")
                return True, self.printer_status, self.status_color
            else:
                self.printer_status = "● Impresora con problemas"
                self.status_color = ("orange", "orange")
                return False, self.printer_status, self.status_color
        except Exception as e:
            self.printer_status = f"● Error de conexión: {str(e)}"
            self.status_color = ("red", "red")
            return False, self.printer_status, self.status_color

    def save_pdf(self, img, output_folder="tickets_pdf"):
        """Guardar imagen como PDF (separado de la impresión)"""
        try:
            os.makedirs(output_folder, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            pdf_path = os.path.join(output_folder, f"ticket_{timestamp}.pdf")
            
            img_rgb = img.convert("RGB") if img.mode in ("RGBA", "P") else img
            img_rgb.save(pdf_path, "PDF", resolution=203)
            
            print(f"✔ PDF guardado en: {pdf_path}")
            return True, pdf_path
        except Exception as e:
            raise Exception(f"Error al guardar PDF: {str(e)}")

    def print_image(self, img, is_test=False):
        """Enviar imagen a la impresora física"""
        if not self.selected_printer:
            raise Exception("No hay impresora seleccionada")
        
        try:
            width_mm, height_mm, dpi = 80, 210, 203
            width_px = int(width_mm * dpi / 25.4)
            height_px = int(height_mm * dpi / 25.4)
            
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(self.selected_printer)
            hdc.StartDoc("Ticket de Prueba" if is_test else "Ticket")
            hdc.StartPage()
            
            dib = ImageWin.Dib(img)
            dib.draw(hdc.GetHandleOutput(), (0, 0, width_px, height_px))
            
            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
            
            return True
        except Exception as e:
            raise Exception(f"Error durante la impresión: {str(e)}")