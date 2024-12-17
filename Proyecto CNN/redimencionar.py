from PIL import Image, ImageEnhance
import os

# Rutas de entrada
input_folders = [
    "C:\\devs\\datasets\\dataset50rotado2\\ferrari",
    "C:\\devs\\datasets\\dataset50rotado2\\hummer",
    "C:\\devs\\datasets\\dataset50rotado2\\vocho",
    "C:\\devs\\datasets\\dataset50rotado2\\mclaren",
    "C:\\devs\\datasets\\dataset50rotado2\\porsche"
]

# Carpetas de salida
output_folders = [
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\ferrari",
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\hummer",
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\vocho",
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\mclaren",
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\porsche"
]

# Crear carpetas de salida si no existen
for output_folder in output_folders:
    os.makedirs(output_folder, exist_ok=True)

# Factores de iluminación y opacidad
brightness_factors = [0.5, 1.5]  # Oscuro y brillante
opacity_factors = [0.5, 1.5]  # Más opaco y más claro

# Procesar imágenes en cada carpeta
for input_folder, output_folder in zip(input_folders, output_folders):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):  # Filtrar formatos soportados
            input_path = os.path.join(input_folder, filename)
            
            try:
                with Image.open(input_path) as img:
                    # Asegurar que la imagen tenga tamaño 50x50
                    img = img.resize((50, 50))
                    
                    # Guardar imagen original en la carpeta de salida
                    img.save(os.path.join(output_folder, f"original_{filename}"))

                    # Aplicar diferentes niveles de brillo
                    for brightness in brightness_factors:
                        enhancer = ImageEnhance.Brightness(img)
                        bright_img = enhancer.enhance(brightness)
                        bright_output_path = os.path.join(output_folder, f"brightness_{brightness}_{filename}")
                        bright_img.save(bright_output_path)

                    # Aplicar diferentes niveles de opacidad (ajuste de saturación de color)
                    for opacity in opacity_factors:
                        enhancer = ImageEnhance.Color(img)
                        opacity_img = enhancer.enhance(opacity)
                        opacity_output_path = os.path.join(output_folder, f"opacity_{opacity}_{filename}")
                        opacity_img.save(opacity_output_path)

                print(f"Procesada: {filename} en {output_folder}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")

print("Proceso completado.")
