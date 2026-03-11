# formats/formato9.py
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoDescansoMedico(BaseTicketFormat):
    """Formato 9: Regularización de Descanso Médico"""
    
    def get_format_name(self):
        return "MED_Descanso_Medico"
    
    def get_required_fields(self):
        """Campos ordenados para encajar en tu UI de 2 columnas"""
        return [
            # FILA 1
            {'name': 'establecimiento', 'label': 'ESTABLECIMIENTO DE SALUD:', 'type': 'text', 'required': True, 'width': 280},
            {'name': 'acto_medico', 'label': 'ACTO MÉDICO:', 'type': 'text', 'required': True, 'width': 280},
            # FILA 2
            {'name': 'tipo_atencion', 'label': 'TIPO DE ATENCIÓN:', 'type': 'radio', 'options': ['CONSULTA EXTERNA'], 'required': True, 'width': 280},
            {'name': 'contingencia', 'label': 'CONTINGENCIA:', 'type': 'radio', 'options': ['ENFERMEDAD COMÚN', 'ACCIDENTE COMÚN', 'ACCIDENTE TRÁNSITO'], 'required': True, 'width': 280},
            # FILA 3
            {'name': 'dias', 'label': 'DÍAS OTORGADOS:', 'type': 'number', 'required': True, 'width': 280},
            {'name': 'servicio', 'label': 'SERVICIO:', 'type': 'text', 'required': True, 'width': 280},
            # FILA 4
            {'name': 'diag1', 'label': 'DIAGNÓSTICO CIE-10 (1°):', 'type': 'autocomplete', 'required': True, 'width': 280},
            {'name': 'diag2', 'label': 'DIAGNÓSTICO CIE-10 (2°):', 'type': 'autocomplete', 'required': False, 'width': 280},
            # FILA 5
            {'name': 'dni', 'label': 'D.N.I. / C.E.:', 'type': 'api_dni', 'target': 'nombres', 'required': True, 'width': 200},
            {'name': 'acc_trabajo', 'label': 'ACC. TRABAJO:', 'type': 'radio', 'options': ['SIN SCTR', 'CON SCTR'], 'required': True, 'width': 280},
            # FILA 6
            {'name': 'nombres', 'label': 'NOMBRES Y APELLIDOS:', 'type': 'text', 'required': True, 'width': 280},
            # FILA 7
            {'name': 'fecha_inicio', 'label': 'FECHA INICIO:', 'type': 'date', 'required': True, 'width': 200},
            {'name': 'fecha_termino', 'label': 'FECHA TÉRMINO:', 'type': 'date', 'required': True, 'width': 200}
        ]
    
    def generate_image(self, data: dict, **kwargs):
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 22)
            font_bold = ImageFont.truetype("arialbd.ttf", 18)
            font_normal = ImageFont.truetype("arial.ttf", 18)
        except:
            font_title = font_bold = font_normal = ImageFont.load_default()
            
        y_pos = 20
        margen_x = 30
        
        # 1. TÍTULO
        tit = "FORMATO DE REGULARIZACIÓN"
        tit2 = "DE DESCANSO MÉDICO"
        draw.text(((self.width_px - draw.textlength(tit, font=font_title)) / 2, y_pos), tit, fill='black', font=font_title)
        y_pos += 30
        draw.text(((self.width_px - draw.textlength(tit2, font=font_title)) / 2, y_pos), tit2, fill='black', font=font_title)
        y_pos += 60
        
        # Función auxiliar para dibujar texto con variable al lado
        def draw_linea(label, valor, y):
            draw.text((margen_x, y), label, fill='black', font=font_bold)
            ancho_label = draw.textlength(label, font=font_bold)
            draw.text((margen_x + ancho_label + 10, y), str(valor), fill='black', font=font_normal)

        # Función auxiliar para dibujar un checkbox
        def draw_checkbox(label, seleccionado, y):
            draw.text((margen_x + 20, y), label, fill='black', font=font_normal)
            ancho = draw.textlength(label, font=font_normal)
            box_x = margen_x + 20 + ancho + 15
            # Dibujar cuadradito
            draw.rectangle([box_x, y, box_x + 20, y + 20], outline='black', width=2)
            if seleccionado == label:
                # Dibujar X
                draw.line([box_x, y, box_x + 20, y + 20], fill='black', width=2)
                draw.line([box_x + 20, y, box_x, y + 20], fill='black', width=2)

        # 2. ESTABLECIMIENTO Y ACTO MÉDICO
        draw_linea("ESTABLECIMIENTO DE SALUD:", data.get('establecimiento', ''), y_pos)
        y_pos += 35
        draw_linea("ACTO MÉDICO:", data.get('acto_medico', ''), y_pos)
        y_pos += 50
        
        # 3. TIPO DE ATENCIÓN
        draw.text((margen_x, y_pos), "TIPO DE ATENCIÓN:", fill='black', font=font_bold)
        y_pos += 30
        draw_checkbox("CONSULTA EXTERNA", data.get('tipo_atencion', ''), y_pos)
        y_pos += 50
        
        # 4. CONTINGENCIA
        draw.text((margen_x, y_pos), "CONTINGENCIA:", fill='black', font=font_bold)
        y_pos += 30
        for opt in ['ENFERMEDAD COMÚN', 'ACCIDENTE COMÚN', 'ACCIDENTE TRÁNSITO']:
            draw_checkbox(opt, data.get('contingencia', ''), y_pos)
            y_pos += 30
        y_pos += 20
        
        # 5. DÍAS OTORGADOS
        draw_linea("DÍAS OTORGADOS:", data.get('dias', ''), y_pos)
        y_pos += 50
        
        # 6. DIAGNÓSTICO CIE-10
        draw.text((margen_x, y_pos), "DIAGNÓSTICO CIE-10:", fill='black', font=font_bold)
        y_pos += 30
        # Extraer solo el código antes del guion del autocompletado si existe
        diag1 = data.get('diag1', '').split(' - ')[0] if data.get('diag1') else ''
        diag2 = data.get('diag2', '').split(' - ')[0] if data.get('diag2') else ''
        
        draw_linea("1°", diag1, y_pos)
        y_pos += 30
        if diag2:
            draw_linea("2°", diag2, y_pos)
            y_pos += 30
        y_pos += 20
        
        # 7. SERVICIO, NOMBRE, DNI
        draw_linea("SERVICIO:", data.get('servicio', ''), y_pos)
        y_pos += 35
        draw_linea("NOMBRES Y APELLIDOS:", data.get('nombres', ''), y_pos)
        y_pos += 35
        draw_linea("D.N.I. / C.E.:", data.get('dni', ''), y_pos)
        y_pos += 50
        
        # 8. ACCIDENTE TRABAJO
        draw.text((margen_x, y_pos), "ACC. TRABAJO:", fill='black', font=font_bold)
        y_pos += 30
        for opt in ['SIN SCTR', 'CON SCTR']:
            draw_checkbox(opt, data.get('acc_trabajo', ''), y_pos)
            y_pos += 30
        y_pos += 20
        
        # 9. FECHAS
        draw_linea("FECHA INICIO:", data.get('fecha_inicio', ''), y_pos)
        y_pos += 35
        draw_linea("FECHA TÉRMINO:", data.get('fecha_termino', ''), y_pos)
        y_pos += 100
        
        # 10. FIRMA
        x_firma = self.width_px / 2
        draw.line([(x_firma - 120, y_pos), (x_firma + 120, y_pos)], fill='black', width=1)
        y_pos += 10
        draw.text((x_firma - 70, y_pos), "FIRMA Y SELLO", fill='black', font=font_normal)
        
        return img