# formats/formato2.py (actualizado)
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoAtencionLaboratorio(BaseTicketFormat):
    """Formato 2: Atención Laboratorio"""
    
    def get_format_name(self):
        return "Atención_Laboratorio"
    
    def get_required_fields(self):
        """Campos requeridos para este formato (NO usa DNI, usa otros campos)"""
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
                'type': 'number',
                'required': True,
                'width': 100,
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
        
        # TÍTULO
        titulo = "HOSPITAL BICENTENARIO CHAO"
        text_width = draw.textlength(titulo, font=font_title)
        draw.text(((self.width_px - text_width) // 2.5, y_position), 
                 titulo, fill='black', font=font_title)
        y_position += 35

         # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=2)
        y_position += 20

        # TÍTULO
        titulo = "ATENCION LABORATORIO"
        text_width = draw.textlength(titulo, font=font_title)
        draw.text(((self.width_px - text_width) // 2.5, y_position), 
                 titulo, fill='black', font=font_title)
        y_position += 35
        
        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=2)
        y_position += 20
        
        # DATOS DEL PACIENTE
        draw.text((30, y_position), "PACIENTE:", fill='black', font=font_bold)
        draw.text((30, y_position+25), nombre_paciente if nombre_paciente else "________________", 
                 fill='black', font=font_normal)
        y_position += 60
        
        draw.text((30, y_position), "DNI:", fill='black', font=font_bold)
        draw.text((80, y_position), dni if dni else "____", 
                 fill='black', font=font_normal2)
        

        draw.text((220, y_position), "SOLICITUD :", fill='black', font=font_bold)
        draw.text((360, y_position), solicitud if solicitud else "____", 
                 fill='black', font=font_normal2)
        y_position += 40
        
         #draw.text((30, y_position), "DIAGNÓSTICO:", fill='black', font=font_bold)
         #y_position += 20
        # Mostrar diagnóstico en múltiples líneas si es largo
         #diagnostico_lines = self.wrap_text(nombre_paciente, 40)
         #for line in diagnostico_lines:
         #   draw.text((40, y_position), line, fill='black', font=font_normal)
          #   y_position += 18
        
       
        
        draw.text((30, y_position), "SERVICIO  :", fill='black', font=font_bold)
        draw.text((150, y_position), servicio_solicitante if servicio_solicitante else "________________", 
                 fill='black', font=font_normal)
        y_position += 40
        
        draw.text((30, y_position), "EXAMEN   :", fill='black', font=font_bold)
        draw.text((150, y_position), examen_solicitado if servicio_solicitante else "________________", 
                 fill='black', font=font_normal)
        y_position += 40

        draw.text((30, y_position), "FECHA   :", fill='black', font=font_bold)
        draw.text((150, y_position), fecha, fill='black', font=font_normal2)
        y_position += 40
        
        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=1)
        y_position += 120
        
        """ MEDICAMENTOS
        draw.text((center_x - 60, y_position), "MEDICAMENTOS", fill='black', font=font_bold)
        y_position += 25
        
        Aquí podrías agregar medicamentos desde los datos si los tienes
        for i in range(4):
            draw.text((40, y_position), f"{i+1}. _________________________", 
                     fill='black', font=font_normal)
            y_position += 20
        
        y_position += 10
        
        INSTRUCCIONES
        draw.text((30, y_position), "INSTRUCCIONES:", fill='black', font=font_bold)
        y_position += 20
        
        instrucciones = [
            "1. Tomar según indicaciones",
            "2. No exceder la dosis",
            "3. Consultar ante efectos adversos"
        ]
        
        for instruccion in instrucciones:
            draw.text((40, y_position), instruccion, fill='black', font=font_normal)
            y_position += 18
        
        y_position += 15 """
        
        # FIRMA
        draw.line([(center_x - 100, y_position), (center_x + 100, y_position)], 
                 fill='black', width=1)
        y_position += 15
        draw.text((center_x - 40, y_position), "Firma del Médico", 
                 fill='black', font=font_normal)
        
        return img
    
    def wrap_text(self, text, max_length):
        """Dividir texto en líneas de máximo max_length caracteres"""
        if not text:
            return []
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= max_length:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines