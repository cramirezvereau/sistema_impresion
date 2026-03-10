# FormatoPruebaHepatitisB
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso"""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FormatoPruebaHepatitisB(BaseTicketFormat):
    """Formato Ticket: Resultado Prueba Rápida HepatitisB (formato compacto)"""
    
    def get_format_name(self):
        return "Resultado_Prueba_Rapida_HepatitisB_Ticket"
    
    def get_required_fields(self):
        """Campos requeridos para este formato"""
        return [
            {
                'name': 'iniciales',
                'label': 'INICIALES',
                'type': 'text',
                'required': True,
                'width': 100,
                'tooltip': 'Iniciales del Paciente'
            },
            {
                'name': 'dni',
                'label': 'DNI',
                'type': 'dni',  # Cambiado a 'dni' para validación automática
                'required': True,
                'width': 150,
                'tooltip': 'Documento Nacional de Identidad'
            },
            {
                'name': 'fecha_prueba',
                'label': 'FECHA PRUEBA',
                'type': 'date',
                'required': True,
                'width': 150,
                'tooltip': 'Fecha de realización de la prueba'
            },
            {
                'name': 'fecha_nacimiento',  # NUEVO CAMPO
                'label': 'FECHA NACIMIENTO',
                'type': 'date',
                'required': True,
                'width': 150,
                'tooltip': 'Fecha de nacimiento del paciente'
            },
            {
                'name': 'edad',
                'label': 'EDAD',
                'type': 'edad',
                'required': True,
                'width': 100,
                'tooltip': 'Edad del paciente'
            },
            {
                'name': 'sexo',
                'label': 'SEXO',
                'type': 'sexo',
                'required': True,
                'width': 100,
                'tooltip': 'Sexo del paciente'
            },
            {
                'name': 'motivo_solicitud',  # NUEVO CAMPO - COMBO
                'label': 'MOTIVO SOLICITUD',
                'type': 'combo',
                'required': True,
                'width': 180,
                'options': [
                    {'value': 'A', 'label': 'A - CONDUCTA DE RIESGO'},
                    {'value': 'B', 'label': 'B - OTROS'}
                ],
                'tooltip': 'Seleccione motivo de solicitud'
            },
            {
                'name': 'resultado_hepatitisB',  # NUEVO CAMPO - COMBO
                'label': 'RESULTADO PRUEBA HepatitisB',
                'type': 'combo',
                'required': True,
                'width': 180,
                'options': [
                    {'value': 'A', 'label': 'A - REACTIVA'},
                    {'value': 'B', 'label': 'B - NO REACTIVA'}
                ],
                'tooltip': 'Seleccione resultado'
            }
        ]
    
    def generate_image(self, data: dict, **kwargs):
        # Obtener datos
        iniciales = data.get('iniciales', '')
        dni = data.get('dni', '')
        fecha_prueba = data.get('fecha_prueba', '')
        fecha_nacimiento = data.get('fecha_nacimiento', '')
        edad = data.get('edad', '')
        sexo = data.get('sexo', '')
        motivo_solicitud = data.get('motivo_solicitud', '')
        resultado_hepatitisB = data.get('resultado_hepatitisB', '')
        
        # Crear imagen
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        # Configurar fuentes
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 25)
            font_bold = ImageFont.truetype("arialbd.ttf", 20)
            font_normal = ImageFont.truetype("arial.ttf", 17)
            font_small = ImageFont.truetype("arial.ttf", 14)
        except:
            font_title = ImageFont.load_default()
            font_bold = ImageFont.load_default()
            font_normal = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        y_position = 20
        center_x = self.width_px // 2
        
        # ============================================
        # LOGO DEL HOSPITAL (CENTRADO)
        # ============================================
        try:
            # Cargar logo
            logo_path = resource_path("images/logo.png")
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                
                # Redimensionar logo
                max_logo_height = 70
                logo_aspect_ratio = logo_image.width / logo_image.height
                new_logo_width = int(max_logo_height * logo_aspect_ratio)
                logo_image = logo_image.resize((new_logo_width, max_logo_height), Image.Resampling.LANCZOS)
                
                # Centrar logo
                logo_x = (self.width_px - new_logo_width) // 3
                logo_y = 10
                img.paste(logo_image, (logo_x, logo_y))
                
                y_position = logo_y + max_logo_height + 10
            else:
                y_position = 20
                
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
            y_position = 20
        
        # ============================================
        # 1. ENCABEZADO - HOSPITAL
        # ============================================
        hospital_text = "HOSPITAL BICENTENARIO DE CHAO"
        text_width_hospital = draw.textlength(hospital_text, font=font_title)
        x_hospital = (self.width_px - text_width_hospital) // 3
        draw.text((x_hospital, y_position), hospital_text, fill='black', font=font_title)
        y_position += 25
        
        # ============================================
        # 2. TÍTULO PRINCIPAL
        # ============================================
        titulo_text = "RESULTADO PRUEBA RAPIDA HEPATITIS B"
        text_width_titulo = draw.textlength(titulo_text, font=font_bold)
        x_titulo = (self.width_px - text_width_titulo) // 3
        draw.text((x_titulo, y_position), titulo_text, fill='black', font=font_bold)
        y_position += 30
        
        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=1)
        y_position += 10
        
        # ============================================
        # 3. DATOS DEL PACIENTE
        # ============================================
        draw.text((40, y_position), "DATOS DEL PACIENTE:", fill='black', font=font_bold)
        y_position += 35
        
        # Iniciales del paciente y DNI
        draw.text((40, y_position), "INICIALES PACIENTE: ", fill='black', font=font_bold)
        draw.text((250, y_position), f" {iniciales if iniciales else '.....'}", fill='black', font=font_bold)
        y_position += 30
        
        draw.text((40, y_position), "DNI: ", fill='black', font=font_bold)
        draw.text((250, y_position), f"{dni if dni else '......'}", fill='black', font=font_bold)
        y_position += 30
        
        # Fecha de nacimiento, Edad y Sexo
        fecha_nac_text = f"FECHA NACIMIENTO: {fecha_nacimiento if fecha_nacimiento else '......'}"
        draw.text((40, y_position), fecha_nac_text, fill='black', font=font_bold)  
        y_position += 30
        
        draw.text((40, y_position), f"EDAD: {edad if edad else '......'}", fill='black', font=font_bold)
        draw.text((250, y_position), f"SEXO: {sexo if sexo else '......'}", fill='black', font=font_bold)
        y_position += 50
        
        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=1)
        y_position += 10
        
        # ============================================
        # 4. FECHA DE PRUEBA
        # ============================================
        draw.text((40, y_position), "DATOS DE LA PRUEBA:", fill='black', font=font_bold)
        y_position += 40
        
        draw.text((40, y_position), "FECHA DE PRUEBA:", fill='black', font=font_bold)
        draw.text((280, y_position), fecha_prueba if fecha_prueba else "______", fill='black', font=font_bold)
        y_position += 30
        
        # ============================================
        # 5. MOTIVO DE SOLICITUD
        # ============================================
        draw.text((40, y_position), "MOTIVO SOLICITUD:", fill='black', font=font_bold)
        motivo_text = "______"
        if motivo_solicitud == 'A':
            motivo_text = "CONDUCTA DE RIESGO"
        elif motivo_solicitud == 'B':
            motivo_text = "OTROS"
        draw.text((280, y_position), motivo_text, fill='black', font=font_bold)
        y_position += 25
        
        # ============================================
        # 6. RESULTADO HepatitisB
        # ============================================
        draw.text((40, y_position), "PRUEBA HEPATITIS B: ", fill='black', font=font_bold)
        hepatitisB_text = "______"
        if resultado_hepatitisB == 'A':
            hepatitisB_text = "REACTIVA"
        elif resultado_hepatitisB == 'B':
            hepatitisB_text = "NO REACTIVA"
        draw.text((280, y_position), hepatitisB_text, fill='black', font=font_bold)
        
        y_position += 35
        
        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=1)
        y_position += 200
        
        # ============================================
        # 7. FIRMA Y SELLO
        # ============================================
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=1)
        firma_text = "Firma y Sello del profesional"
        text_width_firma = draw.textlength(firma_text, font=font_small)
        x_firma = (self.width_px - text_width_firma) // 2
        draw.text((x_firma, y_position), firma_text, fill='black', font=font_normal)
        
        return img