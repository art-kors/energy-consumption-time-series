import matplotlib.pyplot as plt
import numpy as np
import pickle
import functional as F
from library.functional import extract_features


class Layer:
    def __init__(self, input_size, output_size) -> None:
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.bias = np.zeros((1, output_size))


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size) -> None:
        # Инициализация весов и смещений
        self.layer1 = Layer(input_size, hidden_size)
        self.layer2 = Layer(hidden_size, output_size)

    def activation(self, x):
        return 0 if x.any() < 0 else x #ReLU

    def activation_derivative(self, x) -> int:
        return 0 if x.any() < 0 else 1

    def feedforward(self, X):
        self.Z1 = np.dot(X, self.layer1.weights) + self.layer1.bias
        self.A1 = self.activation(self.Z1)
        self.Z2 = np.dot(self.A1, self.layer2.weights) + self.layer2.bias
        self.A2 = self.activation(self.Z2)
        return self.A2

    def backpropagate(self, X, y, learning_rate) -> None:
        m = X.shape[0]
        output_error = self.A2 - y
        dZ2 = output_error * self.activation_derivative(self.A2)
        dW2 = np.dot(self.A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m

        dZ1 = np.dot(dZ2, self.layer2.weights.T) * self.activation_derivative(self.A1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m

        self.layer2.weights -= learning_rate * dW2
        self.layer2.bias -= learning_rate * db2
        self.layer1.weights -= learning_rate * dW1
        self.layer1.bias -= learning_rate * db1

    def train(self, X, y, epochs=10000, learning_rate=0.1) -> None:
        for epoch in range(epochs):
            self.feedforward(X)
            self.backpropagate(X, y, learning_rate)
            if epoch % 1000 == 0:
                np.mean((y - self.A2) ** 2)

    def predict(self, X):
        return self.feedforward(X)


def plotter(x, y, name) -> bool:
    try:
        plt.plot(x, y)
        plt.savefig(name)
    except Exception:
        return False
    return True


def data_to_plot(company_name, predict=False) -> None:
    X, y = F.extract_features(company_name)
    X = X["year"].tolist()  # for example
    y = y.tolist()
    plotter(X, y, company_name + " Energy Consumption.png")


def save_model(X, y, filename):
    #TODO: train model
    model = 0
    with open(f'{filename}.pickle', 'wb') as f:
        pickle.dumps(model, f)


#X, y = extract_features('AEP', 12, 15, '2004-12-31', '2005-12-31')
#print('starting')
#save_model(X, y, 'model')
