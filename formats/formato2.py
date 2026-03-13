# formats/formato2.py
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoAtencionLaboratorio(BaseTicketFormat):
    """Formato 2: Atención Laboratorio"""
    
    def get_format_name(self):
        return "Atención_Laboratorio"
    
    def get_required_fields(self):
        """Campos requeridos para este formato"""
        return [
            {
                'name': 'nombre_paciente',
                'label': 'NOMBRE DEL PACIENTE',
                'type': 'text',
                'required': True,
                'width': 400,
                'tooltip': 'Nombre completo del paciente'
            },
            {
                'name': 'dni',
                'label': 'DNI',
                'type': 'api_dni',
                'target': 'nombre_paciente',
                'required': True,
                'width': 300,
                'tooltip': 'DNI del paciente'
            },
            {
                'name': 'solicitud',
                'label': 'NRO SOLICITUD',
                'type': 'number',
                'required': True,
                'width': 100,
                'tooltip': 'Número de Solicitud'
            },
            {
                'name': 'servicio_solicitante',
                'label': 'SERVICIO',
                'type': 'text',
                'required': True,
                'width': 400,
                'tooltip': 'Servicio Solicitante'
            },
            {
                'name': 'examen_solicitado',
                'label': 'EXAMEN',
                'type': 'text',
                'required': True,
                'width': 300,
                'tooltip': 'Examen Solicitado'
            },
            {
                'name': 'fecha',
                'label': 'FECHA',
                'type': 'date',
                'required': True,
                'width': 180,
                'tooltip': 'Fecha de la Solicitud'
            }
        ]
    
    def generate_image(self, data: dict, **kwargs):
        nombre_paciente = data.get('nombre_paciente', '')
        dni = data.get('dni', '')
        solicitud = data.get('solicitud', '')
        servicio_solicitante = data.get('servicio_solicitante', '')
        examen_solicitado = data.get('examen_solicitado', '')
        fecha = data.get('fecha', '')
        
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        # Configurar fuentes
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 26)
            font_normal = ImageFont.truetype("arial.ttf", 24)
            font_normal2 = ImageFont.truetype("arial.ttf", 26)
            font_bold = ImageFont.truetype("arialbd.ttf", 22)
        except:
            font_title = ImageFont.load_default()
            font_normal = ImageFont.load_default()
            font_normal2 = ImageFont.load_default()
            font_bold = ImageFont.load_default()
        
        y_position = 20
        center_x = self.width_px // 2
        margen_x = 30
        
        # TÍTULOS
        titulo = "HOSPITAL BICENTENARIO CHAO"
        text_width = draw.textlength(titulo, font=font_title)
        draw.text(((self.width_px - text_width) // 2, y_position), titulo, fill='black', font=font_title)
        y_position += 40

        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=2)
        y_position += 20

        titulo2 = "ATENCIÓN LABORATORIO"
        text_width2 = draw.textlength(titulo2, font=font_title)
        draw.text(((self.width_px - text_width2) // 2, y_position), titulo2, fill='black', font=font_title)
        y_position += 40
        
        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=2)
        y_position += 30
        
        # ================= FUNCIÓN PARA ALINEACIÓN PERFECTA =================
        # Fijamos el inicio de los valores en el pixel 160 (para que quepa la palabra SERVICIO:)
        x_valores = 160 
        
        def draw_alineado(label, valor, y, fuente_valor=font_normal):
            draw.text((margen_x, y), label, fill='black', font=font_bold)
            
            ancho_maximo = self.width_px - x_valores - 20
            palabras = str(valor).split()
            lineas = []
            linea_actual = ""
            
            for palabra in palabras:
                prueba = f"{linea_actual} {palabra}".strip()
                if draw.textlength(prueba, font=fuente_valor) <= ancho_maximo:
                    linea_actual = prueba
                else:
                    if linea_actual: lineas.append(linea_actual)
                    linea_actual = palabra
            if linea_actual: lineas.append(linea_actual)
            if not lineas: lineas = [""]
            
            y_actual = y
            for linea in lineas:
                draw.text((x_valores, y_actual), linea, fill='black', font=fuente_valor)
                y_actual += 30 # Altura de línea
            
            return y_actual + 15
        
        # ================= DATOS DEL PACIENTE =================
        # Fila especial: Nombre ocupa todo el ancho y hace salto
        draw.text((margen_x, y_position), "PACIENTE:", fill='black', font=font_bold)
        y_position += 30
        
        ancho_max_nombre = self.width_px - (margen_x * 2)
        palabras_nombre = str(nombre_paciente).split()
        linea_nombre = ""
        for palabra in palabras_nombre:
            prueba = f"{linea_nombre} {palabra}".strip()
            if draw.textlength(prueba, font=font_normal) <= ancho_max_nombre:
                linea_nombre = prueba
            else:
                draw.text((margen_x, y_position), linea_nombre, fill='black', font=font_normal)
                y_position += 30
                linea_nombre = palabra
        if linea_nombre:
            draw.text((margen_x, y_position), linea_nombre, fill='black', font=font_normal)
            
        y_position += 45
        
        # Fila DNI y Solicitud (Comparten línea)
        draw.text((margen_x, y_position), "DNI:", fill='black', font=font_bold)
        draw.text((90, y_position), dni if dni else "________", fill='black', font=font_normal2)
        
        draw.text((260, y_position), "SOLICITUD:", fill='black', font=font_bold)
        draw.text((400, y_position), solicitud if solicitud else "____", fill='black', font=font_normal2)
        y_position += 50
        
        # Filas alineadas con salto de línea automático
        y_position = draw_alineado("SERVICIO:", servicio_solicitante if servicio_solicitante else "________________", y_position)
        y_position = draw_alineado("EXAMEN:", examen_solicitado if examen_solicitado else "________________", y_position)
        y_position = draw_alineado("FECHA:", fecha, y_position, font_normal2)
        
        # Línea separadora
        y_position += 10
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=1)
        
        y_position += 120
        
        # FIRMA CENTRADA Y LÍNEA MÁS LARGA
        # Dibujamos línea de 280px (center - 140 a center + 140)
        draw.line([(center_x - 140, y_position), (center_x + 140, y_position)], fill='black', width=2)
        y_position += 15
        
        txt_firma = "Firma del Médico"
        ancho_firma = draw.textlength(txt_firma, font=font_normal)
        draw.text((center_x - (ancho_firma/2), y_position), txt_firma, fill='black', font=font_normal)
        
        return img