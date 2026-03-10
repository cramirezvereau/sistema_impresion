# formats/base_format.py (actualizado con nuevos tipos)
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
from typing import List, Dict

class BaseTicketFormat(ABC):
    """Clase base abstracta para todos los formatos de tickets"""
    
    def __init__(self):
        self.width_mm = 80
        self.height_mm = 210
        self.dpi = 203
        self.width_px = int(self.width_mm * self.dpi / 25.4)
        self.height_px = int(self.height_mm * self.dpi / 25.4)
    
    @abstractmethod
    def generate_image(self, data: Dict, **kwargs):
        """Método abstracto para generar la imagen del ticket"""
        pass
    
    @abstractmethod
    def get_required_fields(self) -> List[Dict]:
        """Obtener lista de campos requeridos para este formato"""
        pass
    
    def validate_data(self, data: Dict):
        """Validar los datos ingresados para este formato"""
        required_fields = self.get_required_fields()
        
        for field in required_fields:
            field_name = field['name']
            field_type = field.get('type', 'text')
            required = field.get('required', False)
            
            if field_name in data:
                value = data.get(field_name, '').strip()
                
                if required and not value:
                    return False, f"El campo '{field['label']}' es requerido"
                
                # Validaciones específicas por tipo
                if value:  # Solo validar si hay valor
                    validation_result = self.validate_field_type(field_type, value, field)
                    if not validation_result[0]:
                        return validation_result
            
            elif required:
                return False, f"El campo '{field['label']}' es requerido"
        
        return True, "Datos válidos"
    
    def validate_field_type(self, field_type: str, value: str, field: Dict):
        """Validar según el tipo de campo"""
        if field_type == 'dni':
            if not value.isdigit():
                return False, f"El DNI solo puede contener números"
            if len(value) != 8:
                return False, f"El DNI debe tener 8 dígitos"
        
        elif field_type == 'number':
            if not value.isdigit():
                return False, f"El campo '{field['label']}' solo puede contener números"
        
        elif field_type == 'edad':
            if not value.isdigit():
                return False, f"La edad debe ser un número"
            edad_num = int(value)
            if edad_num < 0 or edad_num > 100:
                return False, f"La edad debe estar entre 0 y 100 años"
        
        elif field_type == 'single_letter':
            if len(value) != 1:
                return False, f"El campo '{field['label']}' debe ser una sola letra"
            if not value.isalpha():
                return False, f"El campo '{field['label']}' debe ser una letra (A-Z)"
        
        elif field_type == 'sexo':
            value_upper = value.upper()
            if value_upper not in ['M', 'F', 'H', 'MASCULINO', 'FEMENINO']:
                return False, f"Ingrese M (Masculino) o F (Femenino)"
            if len(value) > 1 and value_upper not in ['MASCULINO', 'FEMENINO']:
                return False, f"Ingrese M (Masculino) o F (Femenino)"
        
        return True, "Campo válido"
    
    def save_as_pdf(self, img, data: Dict, folder_name="Fichas_PDF"):
        """Guardar el ticket como archivo PDF"""
        try:
            # Crear nombre de archivo
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Usar DNI o nombre para el nombre del archivo
            dni = data.get('dni', '')
            nombre = data.get('nombre', '')
            
            if dni and dni.strip():
                filename = f"{self.get_format_name()}_{dni}_{fecha_hora}.pdf"
            elif nombre and nombre.strip():
                nombre_limpio = ''.join(c for c in nombre if c.isalnum() or c in (' ', '_')).strip()
                if len(nombre_limpio) > 20:
                    nombre_limpio = nombre_limpio[:20]
                filename = f"{self.get_format_name()}_{nombre_limpio}_{fecha_hora}.pdf"
            else:
                filename = f"{self.get_format_name()}_{fecha_hora}.pdf"
            
            # Crear carpeta si no existe
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            
            pdf_path = os.path.join(folder_name, filename)
            
            # Guardar imagen temporal
            temp_img_path = tempfile.mktemp(suffix='.png')
            img.save(temp_img_path, 'PNG')
            
            # Crear PDF
            c = canvas.Canvas(pdf_path, pagesize=(self.width_mm*mm, self.height_mm*mm))
            img_width = self.width_mm*mm
            img_height = self.height_mm*mm
            
            c.drawImage(temp_img_path, 0, 0, width=img_width, height=img_height)
            c.setTitle(f"{self.get_format_name()} - {dni if dni else 'Sin DNI'}")
            c.setSubject(self.get_format_name())
            c.setAuthor("Sistema de Impresión HB-CHAO")
            
            c.save()
            
            # Eliminar archivo temporal
            try:
                os.remove(temp_img_path)
            except:
                pass
            
            return pdf_path
            
        except Exception as e:
            print(f"Error al guardar PDF: {e}")
            return None
    
    @abstractmethod
    def get_format_name(self):
        """Obtener nombre del formato"""
        pass