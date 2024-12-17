import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

# Configuración de directorio y lectura de imágenes
data_dir = "C:/Users/Yirr/Desktop/TEC 9/Inteligencia Artificial/Proyectos/Autos CNN/New Autos/dataset"  # Cambia esta ruta a donde estén tus imágenes
img_size = (80, 80)

# Leer imágenes y etiquetas
def cargar_datos(data_dir, img_size):
    images = []
    labels = []
    class_names = os.listdir(data_dir)
    class_names.sort()
    
    for label, class_name in enumerate(class_names[:5]):  # Limitar las clases
        class_dir = os.path.join(data_dir, class_name)
        for file_name in os.listdir(class_dir):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(class_dir, file_name)
                try:
                    img = plt.imread(img_path)
                    # Asegurar que tenga 3 canales
                    if len(img.shape) == 2:  # Imagen en escala de grises
                        img = tf.image.grayscale_to_rgb(tf.convert_to_tensor(img))
                    elif img.shape[-1] != 3:  # Imágenes con más de 3 canales
                        continue
                    img_resized = tf.image.resize(img, img_size).numpy()
                    images.append(img_resized)
                    labels.append(label)
                except Exception as e:
                    print(f"Error al procesar la imagen {img_path}: {e}")
    
    return np.array(images), np.array(labels), class_names[:5]

X, y, class_names = cargar_datos(data_dir, img_size)

# Normalizar imágenes y dividir en entrenamiento y prueba
X = X / 255.0
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Construcción de la CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_size[0], img_size[1], 3)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.3),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.4),
    Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Entrenamiento del modelo
history = model.fit(X_train, y_train, epochs=200, validation_split=0.2, batch_size=64)

# Evaluación
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Precisión en prueba: {test_accuracy * 100:.2f}%")

# Informe de clasificación
y_pred = np.argmax(model.predict(X_test), axis=1)
print(classification_report(y_test, y_pred, target_names=class_names))

# Guardar el modelo con timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = r"C:\Users\Yirr\Desktop\TEC 9\Inteligencia Artificial\Proyectos\Autos CNN\model_test"
os.makedirs(save_path, exist_ok=True)  # Crear el directorio si no existe
model_name = f"modelo_autos_{timestamp}.h5"
model.save(os.path.join(save_path, model_name))

print(f"Modelo guardado en: {os.path.join(save_path, model_name)}")
