from PIL import Image
import os

# Rutas de entrada
input_folders = [
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\ferrari",
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\hummer",
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\vocho",
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\mclaren",
    "C:\\devs\\datasets\\dataset50rotadofiltros2\\porsche"
]

# Carpetas de salida
output_folders = [
    "C:\\devs\\datasets\\dataset21x28\\ferrari",
    "C:\\devs\\datasets\\dataset21x28\\hummer",
    "C:\\devs\\datasets\\dataset21x28\\vocho",
    "C:\\devs\\datasets\\dataset21x28\\mclaren",
    "C:\\devs\\datasets\\dataset21x28\\porsche"
]

# Crear carpetas de salida si no existen
for output_folder in output_folders:
    os.makedirs(output_folder, exist_ok=True)

# Dimensiones de redimensionado
target_size = (21, 28)

# Procesar imágenes en cada carpeta
for input_folder, output_folder in zip(input_folders, output_folders):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):  # Filtrar formatos soportados
            input_path = os.path.join(input_folder, filename)
            
            try:
                with Image.open(input_path) as img:
                    # Redimensionar la imagen a 21x28
                    img = img.resize(target_size)
                    
                    # Guardar la imagen redimensionada
                    output_path = os.path.join(output_folder, filename)
                    img.save(output_path)

                print(f"Procesada: {filename} en {output_folder}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")

print("Proceso completado.")
