from PIL import Image
import os

# Rutas de entrada
input_folders = [
    "C:\\devs\\datasets\\dataset50\\ferrari",
    "C:\\devs\\datasets\\dataset50\\hummer",
    "C:\\devs\\datasets\\dataset50\\vocho",
    "C:\\devs\\datasets\\dataset50\\mclaren",
    "C:\\devs\\datasets\\dataset50\\porsche"
]

# Carpetas de salida
output_folders = [
    "C:\\devs\\datasets\\dataset50rotado2\\ferrari",
    "C:\\devs\\datasets\\dataset50rotado2\\hummer",
    "C:\\devs\\datasets\\dataset50rotado2\\vocho",
    "C:\\devs\\datasets\\dataset50rotado2\\mclaren",
    "C:\\devs\\datasets\\dataset50rotado2\\porsche"
]

# Crear carpetas de salida si no existen
for output_folder in output_folders:
    os.makedirs(output_folder, exist_ok=True)

# Ángulos de rotación
rotation_angles = [90, 180, 270]

# Procesar imágenes en cada carpeta
for input_folder, output_folder in zip(input_folders, output_folders):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):  # Filtrar formatos soportados
            input_path = os.path.join(input_folder, filename)
            
            try:
                # Abrir la imagen
                with Image.open(input_path) as img:
                    # Redimensionar a 50x50
                    resized_img = img.resize((50, 50))

                    # Rotar y guardar la imagen para cada ángulo
                    for angle in rotation_angles:
                        rotated_img = resized_img.rotate(angle, resample=Image.BICUBIC)
                        rotated_output_path = os.path.join(output_folder, f"rotated_{angle}_{filename}")
                        rotated_img.save(rotated_output_path)

                print(f"Procesada: {filename} en {output_folder}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")

print("Proceso completado.")
