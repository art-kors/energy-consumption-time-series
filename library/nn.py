import numpy as np
import pandas as pd
from typing import Callable, List, Union
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


class Layer:
    """Базовый класс слоя нейронной сети."""

    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input: np.ndarray) -> np.ndarray:
        """Прямой проход через слой."""
        raise NotImplementedError

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        """Обратный проход (backpropagation)."""
        raise NotImplementedError


class Dense(Layer):
    """Полносвязный слой."""

    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        # Инициализация весов методом Xavier/Glorot
        self.weights = np.random.randn(output_size, input_size) * np.sqrt(2. / (input_size + output_size))
        self.biases = np.zeros((output_size, 1))

    def forward(self, input: np.ndarray) -> np.ndarray:
        self.input = input
        return np.dot(self.weights, self.input) + self.biases

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        # Градиент по весам и смещениям
        weights_gradient = np.dot(output_gradient, self.input.T)
        input_gradient = np.dot(self.weights.T, output_gradient)

        # Обновление параметров
        self.weights = np.subtract(self.weights, learning_rate * weights_gradient, out=self.weights, casting='unsafe')
        self.biases = np.subtract(self.biases, learning_rate * output_gradient, out=self.biases, casting='unsafe')

        return input_gradient


class Activation(Layer):
    """Слой активации с заданной функцией."""

    def __init__(self, activation: Callable[[np.ndarray], np.ndarray],
                 activation_prime: Callable[[np.ndarray], np.ndarray]):
        super().__init__()
        self.activation = activation
        self.activation_prime = activation_prime

    def forward(self, input: np.ndarray) -> np.ndarray:
        self.input = input
        return self.activation(input)

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient * self.activation_prime(self.input)


# Популярные функции активации
class Tanh(Activation):
    def __init__(self):
        def tanh(x):
            return np.tanh(x)

        def tanh_prime(x):
            return 1 - np.tanh(x) ** 2

        super().__init__(tanh, tanh_prime)


class ReLU(Activation):
    def __init__(self):
        def relu(x):
            return np.maximum(0, x)

        def relu_prime(x):
            return (x > 0).astype(float)

        super().__init__(relu, relu_prime)


class Sigmoid(Activation):
    def __init__(self):
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        def sigmoid_prime(x):
            s = sigmoid(x)
            return s * (1 - s)

        super().__init__(sigmoid, sigmoid_prime)


class NeuralNetwork:
    """Нейронная сеть с поддержкой pandas.DataFrame."""

    def __init__(self, layers: List[Layer], loss: Callable[[np.ndarray, np.ndarray], float],
                 loss_prime: Callable[[np.ndarray, np.ndarray], np.ndarray],
                 numeric_features: List[str] = None,
                 categorical_features: List[str] = None):
        self.layers = layers
        self.loss = loss
        self.loss_prime = loss_prime
        self.numeric_features = numeric_features
        self.categorical_features = categorical_features
        self.preprocessor = None


    def predict(self, X: np.ndarray) -> np.ndarray:
        """Предсказание сети (прямой проход)."""
        #if self.preprocessor is None:
        #    raise ValueError("Модель не обучена. Сначала вызовите метод train().")

        predictions = []

        for x in X:
            output = x.reshape(-1, 1)  # преобразуем в вектор-столбец
            for layer in self.layers:
                output = layer.forward(output)
            predictions.append(output.flatten())

        return np.array(predictions)

    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              epochs: int, learning_rate: float, batch_size: int = 32,
              verbose: bool = True):
        """Обучение сети на тренировочных данных."""
        # Подготовка данных
        y_train = np.expand_dims(y_train, 1)

        for epoch in range(epochs):
            error = 0
            # Мини-пакетный градиентный спуск
            for i in range(0, len(X_train), batch_size):
                batch_X = X_train[i:i + batch_size]
                batch_y = y_train[i:i + batch_size]

                batch_error = 0
                for x, y in zip(batch_X, batch_y):
                    # Прямой проход
                    output = x.reshape(-1, 1)
                    for layer in self.layers:
                        output = layer.forward(output)

                    # Вычисление ошибки
                    batch_error += self.loss(y.reshape(-1, 1), output)

                    # Обратный проход
                    grad = self.loss_prime(y.reshape(-1, 1), output)
                    for layer in reversed(self.layers):
                        grad = layer.backward(grad, learning_rate)

                error += batch_error / len(batch_X)

            error /= (len(X_train) / batch_size)
            if verbose:
                print(f"Epoch {epoch + 1}/{epochs}")


# Примеры функций потерь
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.size


def mape(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-8) -> float:
    """
    Вычисляет Mean Absolute Percentage Error (MAPE) в процентах.

    Параметры:
        y_true: Истинные значения (n_samples, 1)
        y_pred: Предсказанные значения (n_samples, 1)
        epsilon: Малая константа для избежания деления на ноль

    Возвращает:
        Среднюю абсолютную процентную ошибку в %
    """
    # Добавляем epsilon для устойчивости
    y_true = np.where(np.abs(y_true) < epsilon, epsilon, y_true)

    return 100 * np.mean(np.abs((y_true - y_pred) / y_true))


def mape_prime(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-8) -> np.ndarray:
    """
    Производная MAPE для backpropagation.

    Параметры:
        y_true: Истинные значения (n_samples, 1)
        y_pred: Предсказанные значения (n_samples, 1)
        epsilon: Малая константа для избежания деления на ноль

    Возвращает:
        Градиент (n_samples, 1)
    """
    # Защита от деления на ноль
    y_true_safe = np.where(np.abs(y_true) < epsilon, epsilon, y_true)

    # Вычисляем знак ошибки
    error_sign = np.sign(y_pred - y_true_safe)

    # Вычисляем масштабирующий множитель
    scale = 100 / (y_true_safe.size * np.abs(y_true_safe))

    return error_sign * scale


def binary_crossentropy(y_true, y_pred):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))


def binary_crossentropy_prime(y_true, y_pred):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return (y_pred - y_true) / (y_pred * (1 - y_pred))
