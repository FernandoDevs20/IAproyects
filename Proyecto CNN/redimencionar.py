import os
import cv2

def resize_images(input_folder, output_folder, size=(50, 50)):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Procesar cada archivo en la carpeta de entrada
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        
        # Leer la imagen
        img = cv2.imread(input_path)
        
        # Si el archivo no es una imagen, continuar
        if img is None:
            print(f"No se pudo leer el archivo: {file_name}. Saltando...")
            continue
        
        # Redimensionar la imagen
        resized_img = cv2.resize(img, size)
        
        # Guardar la imagen redimensionada
        output_path = os.path.join(output_folder, file_name)
        cv2.imwrite(output_path, resized_img)
        print(f"Imagen redimensionada y guardada: {output_path}")

# Ejemplo de uso
input_folder = 'C:\\devs\\IAProyects\\Proyecto CNN\\dataset\\ferrari'  # Cambia esta ruta a tu carpeta de imágenes
output_folder = 'C:\\devs\\IAProyects\\Proyecto CNN\\dataset\\ferrari2'  # Cambia esta ruta a la carpeta de destino
resize_images(input_folder, output_folder)
