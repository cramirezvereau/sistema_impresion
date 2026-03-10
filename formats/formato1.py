# formats/formato1.py (actualizado)
#from .base_format import BaseTicketFormat
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoEvaluacionRiesgo(BaseTicketFormat):
    """Formato 1: Ficha de Evaluación de Riesgo ITS/VH"""
    
    def get_format_name(self):
        return "Ficha_Evaluacion_Riesgo"
    
    def get_required_fields(self):
        """Campos requeridos para este formato"""
        return [
            {
                'name': 'ap',
                'label': 'AP',
                'type': 'single_letter',
                'required': True,
                'width': 100,
                'tooltip': 'Inicial Apellido Paterno'
            },
            {
                'name': 'am',
                'label': 'AM',
                'type': 'single_letter',
                'required': True,
                'width': 100,
                'tooltip': 'Inicial Apellido Materno'
            },
            {
                'name': 'pn',
                'label': '1N',
                'type': 'single_letter',
                'required': True,
                'width': 100,
                'tooltip': 'Inicial Primer Nombre'
            },
            {
                'name': 'sx',
                'label': 'SX',
                'type': 'sexo',
                'required': True,
                'width': 100,
                'tooltip': 'Sexo'
            },
            {
                'name': 'ed',
                'label': 'ED',
                'type': 'edad',
                'required': True,
                'width': 100,
                'tooltip': 'Edad'
            }
        ]
    
    def generate_image(self, data: dict, **kwargs):
        dni = data.get('dni', '')
        ap = data.get('ap', '')
        am = data.get('am', '')
        pn = data.get('pn', '')
        sx = data.get('sx', '')
        ed = data.get('ed', '')
        fecha = data.get('fecha', '')
        
        # Crear imagen
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)

        
        
        # Configurar fuentes
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 20)
            font_bold = ImageFont.truetype("arialbd.ttf", 15)
            font_big = ImageFont.truetype("arialbd.ttf", 28)
            font_big2 = ImageFont.truetype("arialbd.ttf", 44)
        except:
            font_title = ImageFont.load_default()
            font_bold = ImageFont.load_default()
            font_big = ImageFont.load_default()
            font_big2 = ImageFont.load_default()
        
        y_position = 15
        center_x = self.width_px // 2
        
        # ... (resto del código de generación de imagen)
        
        # Mostrar datos ingresados
        if dni:
            draw.text((40, y_position), f"DNI: {ap}", fill='black', font=font_bold)
            y_position += 25

            
        
       
        if fecha:
            draw.text((40, y_position), f"FECHA: {fecha}", fill='black', font=font_bold)
            y_position += 25
        
        
        
        # ============================================
        # 1. ENCABEZADO - FICHA DE EVALUACIÓN
        # ============================================
        # Título principal
        titulo_principal = "FICHA DE EVALUACIÓN DE RIESGO"
        titulo_secundario = "ITS – VIH SIDA"
        
        # Calcular anchos para centrar
        text_width_principal = draw.textlength(titulo_principal, font=font_title)
        text_width_secundario = draw.textlength(titulo_secundario, font=font_title)
        
        x_principal = (self.width_px - text_width_principal) // 2
        x_secundario = (self.width_px - text_width_secundario) // 2
        
        draw.text((x_principal, y_position), titulo_principal, fill='black', font=font_title)
        y_position += 25
        
        draw.text((x_secundario, y_position), titulo_secundario, fill='black', font=font_title)
        y_position += 30
        
        # Línea separadora
        draw.line([(10, y_position), (self.width_px-10, y_position)], fill='black', width=2)
        y_position += 15
        
        # ============================================
        # 2. SUBTÍTULO (Para el paciente)
        # ============================================
        subtitulo = "(Para el paciente)"
        text_width_subtitulo = draw.textlength(subtitulo, font=font_bold)
        x_subtitulo = (self.width_px - text_width_subtitulo) // 2
        draw.text((x_subtitulo, y_position), subtitulo, fill='black', font=font_bold)
        y_position += 25
        
        # ============================================
        # 3. FICHA Nº (Vacío para completar)
        # ============================================
        ficha_text = "FICHA Nº."
        draw.text((center_x - 40, y_position), ficha_text, fill='black', font=font_bold)
        y_position += 25
        
        # Línea para completar número de ficha
        draw.line([(center_x + 10, y_position), (center_x + 100, y_position)], fill='black', width=1)
        y_position += 20
        
        # Línea separadora
        draw.line([(10, y_position), (self.width_px-10, y_position)], fill='black', width=1)
        y_position += 20
        
        # ============================================
        # 4. CÓDIGO DE IDENTIDAD DEL PACIENTE (DNI)
        # ============================================
        codigo_text = "CODIGO DE IDENTIDAD DEL PACIENTE"
        draw.text((center_x - 120, y_position), codigo_text, fill='black', font=font_bold)
        y_position += 25
        
                    
        
        # ============================================
        # 6. SECCIÓN AP AM IN SX ED (Información médica)
        # ============================================
        # Encabezado de sección médica
        ap_rect = [(40, y_position), (100, y_position + 100)]
        draw.rectangle(ap_rect, outline='black', width=2)
        if ap:
            draw.text((50, y_position+30), ap, fill='black', font=font_big2)
            
        am_rect = [(140, y_position), (200, y_position + 100)]
        draw.rectangle(am_rect, outline='black', width=2)
        if am:
            draw.text((150, y_position+30), am, fill='black', font=font_big2)
        n_rect = [(240, y_position), (300, y_position + 100)]
        draw.rectangle(n_rect, outline='black', width=2)
        if pn:
            draw.text((250, y_position+30), pn, fill='black', font=font_big2)
        sx_rect = [(340, y_position), (400, y_position + 100)]
        draw.rectangle(sx_rect, outline='black', width=2)
        if sx:
            draw.text((350, y_position+30), sx, fill='black', font=font_big2)
        ed_rect = [(440, y_position), (500, y_position + 100)]
        draw.rectangle(ed_rect, outline='black', width=2)
        if ed:
            draw.text((445, y_position+30), ed, fill='black', font=font_big2)

        y_position += 100

        draw.text((50, y_position), "AP", fill='black', font=font_big)
            # Línea para completar
        
        draw.text((150, y_position), "AM", fill='black', font=font_big)
            # Línea para completar
        draw.text((250, y_position), "1N", fill='black', font=font_big)
            # Línea para completar
        draw.text((350, y_position), "SX", fill='black', font=font_big)
            # Línea para font_big
        draw.text((445, y_position), "ED", fill='black', font=font_big)
            # Línea para completar
        y_position += 40

        #draw.rectangle(xy='10,10,10,10',fill='black',width=2)
        #draw.circle()

        
        
                
        
        # ============================================
        # 8. PIE DE PÁGINA
        # ============================================
        # Línea final
        draw.line([(10, y_position), (self.width_px-10, y_position)], fill='black', width=2)
        y_position += 120
        
                
        # FIRMA Y SELLO
        firma_line = "-" * 60
        text_width_firma = draw.textlength(firma_line, font=font_bold)
        x_firma = (self.width_px - text_width_firma) // 1.4
        draw.text((x_firma, y_position), firma_line, fill='black', font=font_bold)
        y_position += 15
        draw.text(( x_firma, y_position), "Firma y Sello del profesional", fill='black', font=font_title)
        
        return img