import os
import cv2

def augment_images(input_folder, output_folder, target_size=(50, 50)):
    """
    Aplica transformaciones a las imágenes de la carpeta de entrada, las redimensiona a 50x50 
    y guarda las transformaciones en la carpeta de salida.

    Args:
        input_folder (str): Ruta de la carpeta donde están las imágenes originales.
        output_folder (str): Ruta de la carpeta donde se guardarán las imágenes transformadas.
        target_size (tuple): Tamaño al que se redimensionarán las imágenes (ancho, alto).
    """
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Listar todas las imágenes en la carpeta de entrada
    images = [img for img in os.listdir(input_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

    print(f"Encontradas {len(images)} imágenes en {input_folder}. Aplicando transformaciones...")

    for img_name in images:
        # Leer la imagen
        img_path = os.path.join(input_folder, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"Error al cargar la imagen: {img_path}. Saltando...")
            continue

        # Aplicar transformaciones
        transformations = [
            ('original', img),
            ('rotated_90', cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)),
            ('rotated_180', cv2.rotate(img, cv2.ROTATE_180)),
            ('rotated_270', cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)),
            ('flipped_horizontal', cv2.flip(img, 1)),
            ('flipped_vertical', cv2.flip(img, 0))
        ]

        # Guardar las imágenes transformadas redimensionadas
        for transform_name, transformed_img in transformations:
            resized_img = cv2.resize(transformed_img, target_size, interpolation=cv2.INTER_AREA)
            output_path = os.path.join(output_folder, f"{os.path.splitext(img_name)[0]}_{transform_name}.jpg")
            cv2.imwrite(output_path, resized_img)

    print(f"Transformaciones completadas. Imágenes guardadas en {output_folder}.")

# Ruta de la carpeta de entrada (donde están las imágenes originales)
input_folder = "C:\\devs\\IAProyects\\Proyecto CNN\\dataset\\vocho"

# Ruta de la carpeta de salida (donde se guardarán las imágenes transformadas)
output_folder = "C:\\devs\\IAProyects\\Proyecto CNN\\dataset\\vocho2"

# Llamar a la función
augment_images(input_folder, output_folder)
