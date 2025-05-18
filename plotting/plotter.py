import matplotlib.pyplot as plt
import numpy as np
from core import functional as F
from core.functional import extract_features


class Layer:
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.bias = np.zeros((1, output_size))


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Инициализация весов и смещений
        self.layer1 = Layer(input_size, hidden_size)
        self.layer2 = Layer(hidden_size, output_size)

    def sigmoid(self, x):
        return 0 if x.any() < 0 else x

    def sigmoid_derivative(self, x):
        return 0 if x.any() < 0 else 1

    def feedforward(self, X):
        self.Z1 = np.dot(X, self.layer1.weights) + self.layer1.bias
        self.A1 = self.sigmoid(self.Z1)
        self.Z2 = np.dot(self.A1, self.layer2.weights) + self.layer2.bias
        self.A2 = self.sigmoid(self.Z2)
        return self.A2

    def backpropagate(self, X, y, learning_rate):
        m = X.shape[0]
        output_error = self.A2 - y
        dZ2 = output_error * self.sigmoid_derivative(self.A2)
        dW2 = np.dot(self.A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m

        dZ1 = np.dot(dZ2, self.layer2.weights.T) * self.sigmoid_derivative(self.A1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m

        self.layer2.weights -= learning_rate * dW2
        self.layer2.bias -= learning_rate * db2
        self.layer1.weights -= learning_rate * dW1
        self.layer1.bias -= learning_rate * db1

    def train(self, X, y, epochs=10000, learning_rate=0.1):
        for epoch in range(epochs):
            self.feedforward(X)
            self.backpropagate(X, y, learning_rate)
            if epoch % 1000 == 0:
                loss = np.mean((y - self.A2) ** 2)
                print(f"Epoch {epoch}, Loss: {loss:.4f}")

    def predict(self, X):
        return self.feedforward(X)


def plotter(x, y, name):
    try:
        plt.plot(x, y)
        plt.savefig(name)
    except Exception as e:
        print(e)
        return False
    return True


def data_to_plot(company_name, predict=False):
    X, y = F.extract_features(company_name)
    print('data extraction - complete!')
    print('plotting...')
    X = X['year'].tolist() #for example
    y = y.tolist()
    plotter(X, y, company_name + ' Energy Consuption.png')


#predictor = NeuralNetwork(1, 1, 1)

data_to_plot('AEP')

