# formats/formato3.py
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoAtencionOdontologica(BaseTicketFormat):
    """Formato 3: Atención Odontológica con todas las validaciones"""
    
    def get_format_name(self):
        return "Atención_Odontológica"
    
    def get_required_fields(self):
        """Campos requeridos para este formato"""
        return [
            {
                'name': 'dni',
                'label': 'DNI',
                'type': 'api_dni',
                'target': 'nombre',
                'required': True,
                'width': 200,
                'tooltip': '8 dígitos numéricos'
            },
            {
                'name': 'nombre',
                'label': 'NOMBRE COMPLETO',
                'type': 'text',
                'required': True,
                'width': 400,
                'tooltip': 'Nombre y apellidos'
            },
            {
                'name': 'hora_ingreso',
                'label': 'HORA INGRESO',
                'type': 'hora',  # NUEVO: Campo de hora
                'required': True,
                'width': 120,
                'tooltip': 'Formato: HH:MM:SS (24h)'
            },
            {
                'name': 'fecha',
                'label': 'FECHA',
                'type': 'date',
                'required': True,
                'width': 180,
                'tooltip': 'Fecha de consulta'
            }
        ]
    
    def generate_image(self, data: dict, **kwargs):
        dni = data.get('dni', '')
        nombre = data.get('nombre', '')
        hora_ingreso = data.get('hora_ingreso', '')
        fecha = data.get('fecha', '')
        
        # Mantenemos el lienzo intacto, sin cortes al final para evitar distorsiones
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        # Configurar fuentes un poco más grandes para mejor lectura
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 24)
            font_bold = ImageFont.truetype("arialbd.ttf", 20)
            font_normal = ImageFont.truetype("arial.ttf", 20)
        except:
            font_title = font_bold = font_normal = ImageFont.load_default()
            
        y_position = 20
        margen_x = 30
        
        # TÍTULO
        titulo = "ATENCIÓN ODONTOLÓGICA"
        text_width = draw.textlength(titulo, font=font_title)
        draw.text(((self.width_px - text_width) // 2, y_position), titulo, fill='black', font=font_title)
        y_position += 40
        
        # Línea separadora superior
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=2)
        y_position += 30
        
        # ================= FUNCIÓN PARA ALINEACIÓN PERFECTA =================
        # Fijamos el inicio de TODOS los valores en el pixel 140
        x_valores = 140 
        
        def draw_alineado(label, valor, y):
            # Etiqueta en negrita
            draw.text((margen_x, y), label, fill='black', font=font_bold)
            
            # Texto normal (con salto de línea matemático si es largo)
            ancho_maximo = self.width_px - x_valores - 20
            palabras = str(valor).split()
            lineas = []
            linea_actual = ""
            
            for palabra in palabras:
                prueba = f"{linea_actual} {palabra}".strip()
                if draw.textlength(prueba, font=font_normal) <= ancho_maximo:
                    linea_actual = prueba
                else:
                    if linea_actual: lineas.append(linea_actual)
                    linea_actual = palabra
            if linea_actual: lineas.append(linea_actual)
            if not lineas: lineas = [""]
            
            y_actual = y
            for linea in lineas:
                draw.text((x_valores, y_actual), linea, fill='black', font=font_normal)
                y_actual += 30
            
            return y_actual + 15 # Retorna la nueva posición Y

        # DATOS DEL PACIENTE IMPRESOS COMO TABLA
        y_position = draw_alineado("DNI:", dni if dni else "__________", y_position)
        y_position = draw_alineado("NOMBRE:", nombre, y_position)
        y_position = draw_alineado("FECHA:", fecha, y_position)
        y_position = draw_alineado("HORA:", hora_ingreso, y_position)
        
        # Línea separadora inferior
        y_position += 10
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=2)
        
        y_position += 120
        
        # FIRMA CENTRADA
        center_x = self.width_px // 2
        draw.line([(center_x - 120, y_position), (center_x + 120, y_position)], fill='black', width=2)
        y_position += 15
        
        txt_firma = "Firma del Médico"
        ancho_firma = draw.textlength(txt_firma, font=font_bold)
        draw.text((center_x - (ancho_firma/2), y_position), txt_firma, fill='black', font=font_bold)
        
        return img