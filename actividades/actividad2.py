import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import LabelBinarizer

# Datos de entrenamiento
X = np.array([
    [0.9, 0.8, 0.2],
    [0.7, 0.6, 0.5],
    [0.4, 0.4, 0.8],
    [0.8, 0.9, 0.3],
    [0.5, 0.7, 0.6],
    [0.3, 0.5, 0.9]
])
y = np.array([0, 1, 2, 0, 1, 2])  # 0=Riesgo Bajo, 1=Medio, 2=Alto

# One-hot encoding para las etiquetas
encoder = LabelBinarizer()
y_encoded = encoder.fit_transform(y)

# Crear el modelo
model = Sequential([
    Dense(10, activation='relu', input_shape=(3,)),  # Capa oculta con 10 neuronas
    Dense(3, activation='softmax')                  # Capa de salida con 3 categorías
])

# Compilar el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X, y_encoded, epochs=500, verbose=0)

# Evaluar el modelo
accuracy = model.evaluate(X, y_encoded, verbose=0)[1]
print(f"Precisión del modelo: {accuracy * 100:.2f}%")

# Probar con nuevos datos
new_data = np.array([[0.8, 0.7, 0.4], [0.3, 0.6, 0.8]])
predictions = model.predict(new_data)
predicted_classes = np.argmax(predictions, axis=1)

print("Predicciones para nuevos datos:", predicted_classes)

# Graficar la frontera de decisión (2D simplificado)
x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                     np.arange(y_min, y_max, 0.01))

# Realizar predicciones en la malla
Z = model.predict(np.c_[xx.ravel(), yy.ravel(), np.zeros_like(xx.ravel())])
Z = np.argmax(Z, axis=1)
Z = Z.reshape(xx.shape)

# Graficar
plt.contourf(xx, yy, Z, alpha=0.8, cmap='viridis')
scatter = plt.scatter(X[:, 0], X[:, 1], c=y, edgecolor='k', cmap='viridis', label='Datos')
plt.colorbar(scatter, ticks=[0, 1, 2], label='Categoría de Riesgo')
plt.xlabel('Historial de pagos')
plt.ylabel('Ingresos mensuales')
plt.title('Frontera de decisión - Clasificación de clientes')
plt.show()
