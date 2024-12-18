import numpy as np
import matplotlib.pyplot as plt

# Datos de entrenamiento
X = np.array([
    [0.5, 0.8],
    [0.6, 0.9],
    [0.7, 0.6],
    [0.4, 0.5],
    [0.3, 0.9],
    [0.8, 0.4]
])
y = np.array([1, 1, 0, 0, 1, 0])  # Etiquetas: 1=Aceptado, 0=Rechazado

# Inicialización de parámetros
w = np.random.rand(2)  # Pesos iniciales
b = np.random.rand()   # Sesgo inicial
learning_rate = 0.1    # Tasa de aprendizaje

def step_function(z):
    return 1 if z >= 0 else 0

# Entrenamiento del perceptrón
for epoch in range(100):  # 100 épocas de entrenamiento
    for i in range(len(X)):
        z = np.dot(w, X[i]) + b  # Predicción
        y_pred = step_function(z)
        error = y[i] - y_pred    # Error
        # Actualización de pesos y sesgo
        w += learning_rate * error * X[i]
        b += learning_rate * error

# Graficar datos y frontera de decisión
x_vals = np.linspace(0, 1, 100)
y_vals = -(w[0] * x_vals + b) / w[1]  # Ecuación de la frontera de decisión

plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', label='Datos')
plt.plot(x_vals, y_vals, color='red', label='Frontera de decisión')
plt.xlabel('Precio Relativo')
plt.ylabel('Calidad Percibida')
plt.legend()
plt.title('Clasificación de Productos')
plt.show()
