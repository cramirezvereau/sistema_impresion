from PIL import Image

# Convertir PNG a ICO
img = Image.open('icono.png')

# Crear múltiples tamaños para el icono
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save('icono.ico', sizes=sizes, format='ICO')