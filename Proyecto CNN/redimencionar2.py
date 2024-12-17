from PIL import Image, ImageEnhance
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

# Ángulos de rotación y factor de zoom
rotation_angles = [45, 135,225,315]  # Rotaciones diagonales
zoom_factor = 1.5  # Factor de zoom para eliminar esquinas negras

# Procesar imágenes en cada carpeta
for input_folder, output_folder in zip(input_folders, output_folders):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):  # Filtrar formatos soportados
            input_path = os.path.join(input_folder, filename)
            
            with Image.open(input_path) as img:
                # Asegurar que la imagen tenga tamaño 50x50
                img = img.resize((50, 50))
                
                # Guardar imagen original en la carpeta de salida
                img.save(os.path.join(output_folder, f"original_{filename}"))

                # Aplicar rotaciones con zoom
                for angle in rotation_angles:
                    # Calcular nuevo tamaño con el factor de zoom
                    width, height = img.size
                    zoomed_img = img.resize((int(width * zoom_factor), int(height * zoom_factor)))

                    # Rotar la imagen
                    rotated_img = zoomed_img.rotate(angle, resample=Image.BICUBIC)

                    # Recortar al tamaño original para centrar la imagen
                    left = (rotated_img.width - width) // 2
                    top = (rotated_img.height - height) // 2
                    cropped_img = rotated_img.crop((left, top, left + width, top + height))

                    # Guardar la imagen rotada y recortada
                    output_path = os.path.join(output_folder, f"rotated_{angle}_{filename}")
                    cropped_img.save(output_path)

        print(f"Procesada: {filename} en {output_folder}")

print("Proceso completado.")
