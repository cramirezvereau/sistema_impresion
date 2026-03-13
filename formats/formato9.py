# formats/formato9.py
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoDescansoMedico(BaseTicketFormat):
    """Formato 9: Regularización de Descanso Médico"""
    
    def get_format_name(self):
        return "MED_Descanso_Medico"
    
    def get_required_fields(self):
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
            font_title = ImageFont.truetype("arialbd.ttf", 26)
            font_bold = ImageFont.truetype("arialbd.ttf", 22)
            font_normal = ImageFont.truetype("arial.ttf", 22)
        except:
            font_title = font_bold = font_normal = ImageFont.load_default()
            
        y_pos = 20
        margen_x = 20
        
        def dibujar_separador(y):
            draw.line([(margen_x, y), (self.width_px - margen_x, y)], fill='black', width=2)
            
        # ==========================================
        # FUNCIÓN MAESTRA: Dibuja texto con salto de línea automático
        # ==========================================
        def draw_linea(label, valor, y, salto_base=40):
            # Imprime la etiqueta en negrita
            draw.text((margen_x, y), label, fill='black', font=font_bold)
            ancho_label = draw.textlength(label, font=font_bold)
            
            # Calcula dónde empieza el valor y su límite de ancho
            x_valor = margen_x + ancho_label + 15
            ancho_maximo = self.width_px - x_valor - 20 # 20px margen derecho de seguridad
            
            # Cortamos el texto en palabras y verificamos si caben
            palabras = str(valor).split()
            lineas = []
            linea_actual = ""
            
            for palabra in palabras:
                prueba = f"{linea_actual} {palabra}".strip()
                if draw.textlength(prueba, font=font_normal) <= ancho_maximo:
                    linea_actual = prueba # Si cabe, sumamos la palabra
                else:
                    if linea_actual: lineas.append(linea_actual) # No cabe, guardamos la línea
                    linea_actual = palabra # y la palabra actual baja a la siguiente línea
            if linea_actual: lineas.append(linea_actual)
            if not lineas: lineas = [""]
            
            # Imprimimos las líneas calculadas
            y_actual = y
            for linea in lineas:
                draw.text((x_valor, y_actual), linea, fill='black', font=font_normal)
                y_actual += 30 # Altura que ocupa cada línea
                
            # Devuelve la nueva posición 'y_pos' dependiendo de cuánto creció el texto
            altura_ocupada = y_actual - y
            if altura_ocupada < salto_base:
                return y + salto_base
            return y_actual + 10 # Si ocupó varias líneas, dejamos 10px de margen inferior extra

        def draw_checkbox(label, seleccionado, y):
            draw.text((margen_x + 20, y), label, fill='black', font=font_normal)
            box_x = self.width_px - 70 
            draw.rectangle([box_x, y, box_x + 24, y + 24], outline='black', width=2)
            if seleccionado == label:
                draw.line([box_x, y, box_x + 24, y + 24], fill='black', width=3)
                draw.line([box_x + 24, y, box_x, y + 24], fill='black', width=3)

        # ==========================================
        # TÍTULO
        # ==========================================
        tit = "FORMATO DE REGULARIZACIÓN"
        tit2 = "DE DESCANSO MÉDICO"
        draw.text(((self.width_px - draw.textlength(tit, font=font_title)) / 2, y_pos), tit, fill='black', font=font_title)
        y_pos += 35
        draw.text(((self.width_px - draw.textlength(tit2, font=font_title)) / 2, y_pos), tit2, fill='black', font=font_title)
        y_pos += 50
        
        dibujar_separador(y_pos)
        y_pos += 20
        
        # ==========================================
        # DATOS GENERALES
        # ==========================================
        y_pos = draw_linea("ESTABLECIMIENTO:", data.get('establecimiento', ''), y_pos, 40)
        y_pos = draw_linea("ACTO MÉDICO:", data.get('acto_medico', ''), y_pos, 50)
        
        dibujar_separador(y_pos)
        y_pos += 20
        
        # ==========================================
        # ATENCIÓN Y CONTINGENCIA
        # ==========================================
        draw.text((margen_x, y_pos), "TIPO DE ATENCIÓN:", fill='black', font=font_bold)
        y_pos += 35
        draw_checkbox("CONSULTA EXTERNA", data.get('tipo_atencion', ''), y_pos)
        y_pos += 50
        
        draw.text((margen_x, y_pos), "CONTINGENCIA:", fill='black', font=font_bold)
        y_pos += 35
        for opt in ['ENFERMEDAD COMÚN', 'ACCIDENTE COMÚN', 'ACCIDENTE TRÁNSITO']:
            draw_checkbox(opt, data.get('contingencia', ''), y_pos)
            y_pos += 35
        y_pos += 15
        
        dibujar_separador(y_pos)
        y_pos += 20
        
        # ==========================================
        # DÍAS Y DIAGNÓSTICO
        # ==========================================
        y_pos = draw_linea("DÍAS OTORGADOS:", data.get('dias', ''), y_pos, 45)
        
        draw.text((margen_x, y_pos), "DIAGNÓSTICO CIE-10:", fill='black', font=font_bold)
        y_pos += 35
        
        diag1 = data.get('diag1', '').split(' - ')[0] if data.get('diag1') else ''
        diag2 = data.get('diag2', '').split(' - ')[0] if data.get('diag2') else ''
        
        y_pos = draw_linea(" 1°", diag1, y_pos, 35)
        if diag2:
            y_pos = draw_linea(" 2°", diag2, y_pos, 35)
        y_pos += 15
        
        dibujar_separador(y_pos)
        y_pos += 20
        
        # ==========================================
        # DATOS DEL PACIENTE
        # ==========================================
        y_pos = draw_linea("SERVICIO:", data.get('servicio', ''), y_pos, 40)
        
        # AQUI OCURRE LA MAGIA DEL SALTO DE LINEA SI ES LARGO
        y_pos = draw_linea("NOMBRES:", data.get('nombres', ''), y_pos, 40)
        
        y_pos = draw_linea("D.N.I. / C.E.:", data.get('dni', ''), y_pos, 50)
        
        draw.text((margen_x, y_pos), "ACC. TRABAJO:", fill='black', font=font_bold)
        y_pos += 35
        for opt in ['SIN SCTR', 'CON SCTR']:
            draw_checkbox(opt, data.get('acc_trabajo', ''), y_pos)
            y_pos += 35
        y_pos += 15
        
        dibujar_separador(y_pos)
        y_pos += 20
        
        # ==========================================
        # FECHAS Y FIRMA
        # ==========================================
        y_pos = draw_linea("FECHA INICIO:", data.get('fecha_inicio', ''), y_pos, 40)
        y_pos = draw_linea("FECHA TÉRMINO:", data.get('fecha_termino', ''), y_pos, 40)
        
        y_pos += 120 
        
        x_firma = self.width_px / 2
        draw.line([(x_firma - 140, y_pos), (x_firma + 140, y_pos)], fill='black', width=2)
        y_pos += 10
        draw.text((x_firma - 85, y_pos), "FIRMA Y SELLO", fill='black', font=font_bold)
        y_pos += 40
        
        # Cortamos el ticket de forma segura
        img = img.crop((0, 0, self.width_px, y_pos))
        
        return img