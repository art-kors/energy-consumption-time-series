import matplotlib.pyplot as plt

import functional as F
from library.nn import *


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


# X, y = extract_features('COMED', 0, 23, '2011-12-31', '2016-01-11')
# print(X.shape)

# print(X)

# network = NeuralNetwork([
#    Dense(X.shape[1], X.shape[1]//2),
#    ReLU(),
#    Dense(X.shape[1]//2, X.shape[1]//4),
#    ReLU(),
#    Dense(X.shape[1]//4, 1),
#
# ],
#    loss=mse,
#    loss_prime=mse_prime,
#    numeric_features=[*X.columns])
#
#
#
# network.train(X_train=X[:len(X)//2], y_train=y[:len(X)//2], batch_size=128, epochs=10, learning_rate=0.001)
#
# from sklearn.metrics import mean_absolute_percentage_error
# print(set(np.squeeze(network.predict(X))))
# for i, j in zip(np.squeeze(network.predict(X)), y):
#    print(i, j)
#
# print('MAPE:', mean_absolute_percentage_error(np.squeeze(network.predict(X)), y))
