from ultralytics import YOLO
import cv2
import os

# Cargar el modelo preentrenado YOLOv8 (puedes usar 'yolov8n.pt', 'yolov8s.pt' para mayor precisión)
model = YOLO("yolov8n.pt")

# Ruta del video
video_path = "C:\\devs\\IAProyects\\Proyecto CNN\\dataset\\VIDEOS\\PORSCHE2.mkv"  # Cambia esta ruta por la del video
output_folder = "C:\\devs\\IAProyects\\Proyecto CNN\\dataset\\porsche\\"  # Carpeta donde se guardarán las imágenes detectadas

# Crear la carpeta de salida si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Abrir el video
cap = cv2.VideoCapture(video_path)
frame_count = 0  # Contador para el número de frames procesados
car_count = 0  # Contador para las imágenes de autos extraídas

# Procesar cada frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:  # Salir si no hay más frames
        break

    # Hacer detecciones en el frame
    results = model.predict(source=frame, conf=0.5, classes=[2], verbose=False)  # classes=[2] filtra autos (COCO class ID 2)

    # Extraer y guardar imágenes de los autos detectados
    for box in results[0].boxes.xyxy:  # Coordenadas de las detecciones
        x1, y1, x2, y2 = map(int, box)  # Convertir coordenadas a enteros
        car_crop = frame[y1:y2, x1:x2]  # Recortar la región del auto

        # Guardar la imagen del auto si no está vacía
        if car_crop.size > 0:
            car_filename = os.path.join(output_folder, f"auto_{car_count}.jpg")
            cv2.imwrite(car_filename, car_crop)
            car_count += 1

    # Mostrar el frame procesado con detecciones
    cv2.imshow("Detección de Autos", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

# Liberar el video y cerrar ventanas
cap.release()
cv2.destroyAllWindows()

print(f"Proceso finalizado: {car_count} autos detectados y guardados en '{output_folder}'.")
