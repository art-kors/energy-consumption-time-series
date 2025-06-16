"""ML model module."""

from typing import Self

import numpy as np
from numpy import float32, float64, full, full_like, mean, ndarray


class DecisionTreeRegressor:
    """Decision tree regressor."""

    def __init__(self: Self, max_depth: int = 3) -> None:
        self.max_depth = max_depth
        self.tree = None

    class Node:
        def __init__(
            self: Self,
            feature_idx=None,
            threshold=None,
            left=None,
            right=None,
            value=None,
        ) -> None:
            self.feature_idx = feature_idx
            self.threshold = threshold
            self.left = left
            self.right = right
            self.value = value

    def _mse(self, y: ndarray) -> float32:
        return mean((y - np.mean(y)) ** 2)

    def _best_split(self, X, y):
        best_mse = float("inf")
        best_feature, best_threshold = None, None

        for feature_idx in range(X.shape[1]):
            thresholds = np.unique(X[:, feature_idx])
            for threshold in thresholds:
                left_mask = X[:, feature_idx] <= threshold
                right_mask = ~left_mask

                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                mse = (
                    self._mse(y[left_mask]) * np.sum(left_mask)
                    + self._mse(y[right_mask]) * np.sum(right_mask)
                ) / len(y)

                if mse < best_mse:
                    best_mse = mse
                    best_feature = feature_idx
                    best_threshold = threshold

        return best_feature, best_threshold

    def _build_tree(self, X, y, depth=0):
        if depth >= self.max_depth or len(np.unique(y)) == 1:
            return self.Node(value=np.mean(y))

        feature_idx, threshold = self._best_split(X, y)
        if feature_idx is None:
            return self.Node(value=np.mean(y))

        left_mask = X[:, feature_idx] <= threshold
        right_mask = ~left_mask

        left = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return self.Node(feature_idx, threshold, left, right)

    def fit(self, X, y):
        self.tree = self._build_tree(X, y)

    def _predict_sample(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature_idx] <= node.threshold:
            return self._predict_sample(x, node.left)
        return self._predict_sample(x, node.right)

    def predict(self, X):
        return np.array([self._predict_sample(x, self.tree) for x in X])


class GradientBoostingRegressor:
    """Gradient boosting regressor."""

    def __init__(
        self: Self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
    ) -> None:
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.initial_prediction = None

    def train(self, X, y) -> None:
        # Начальное предсказание - среднее значение y
        self.initial_prediction = mean(y)
        current_pred = full_like(
            y,
            self.initial_prediction,
            dtype=float64,
        )

        for _ in range(self.n_estimators):
            # Вычисляем остатки (антиградиент)
            residuals = y - current_pred

            # Обучаем дерево на остатках
            tree = DecisionTreeRegressor(max_depth=self.max_depth)
            tree.fit(X, residuals)

            # Делаем предсказание и обновляем текущее предсказание
            pred = tree.predict(X)
            current_pred += self.learning_rate * pred
            print(f"Estimator trained {_ + 1}/{self.n_estimators}")
            # Сохраняем дерево
            self.trees.append(tree)

    def predict(self, X):
        # Начинаем с начального предсказания
        y_pred = full(X.shape[0], self.initial_prediction, dtype=float64)

        # Добавляем предсказания всех деревьев
        for tree in self.trees:
            y_pred += self.learning_rate * tree.predict(X)

        return y_pred
