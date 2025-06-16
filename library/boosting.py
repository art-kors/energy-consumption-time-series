"""ML model module."""

from typing import Self

import numpy as np
from numpy import (
    array,
    float32,
    float64,
    full,
    full_like,
    mean,
    ndarray,
    unique,
)


class DecisionTreeRegressor:
    """Decision tree regressor."""

    def __init__(self: Self, max_depth: int = 3) -> None:
        """Construct decision tree regressor."""
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

    def _mse(self: Self, y: ndarray) -> float32:
        return mean((y - np.mean(y)) ** 2)

    def _best_split(self: Self, x: ndarray, y: ndarray) -> tuple:
        best_mse = float("inf")
        best_feature, best_threshold = None, None

        for feature_idx in range(x.shape[1]):
            thresholds = unique(x[:, feature_idx])
            for threshold in thresholds:
                left_mask = x[:, feature_idx] <= threshold
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

    def _build_tree(
        self: Self,
        x: ndarray,
        y: ndarray,
        depth: int = 0,
    ) -> Node:
        if depth >= self.max_depth or len(unique(y)) == 1:
            return self.Node(value=mean(y))

        feature_idx, threshold = self._best_split(x, y)
        if feature_idx is None:
            return self.Node(value=mean(y))

        left_mask = x[:, feature_idx] <= threshold
        right_mask = ~left_mask

        left = self._build_tree(x[left_mask], y[left_mask], depth + 1)
        right = self._build_tree(x[right_mask], y[right_mask], depth + 1)

        return self.Node(feature_idx, threshold, left, right)

    def fit(self: Self, x: ndarray, y: ndarray) -> None:
        self.tree = self._build_tree(x, y)

    def _predict_sample(self: Self, x, node) -> ndarray:
        if node.value is not None:
            return node.value
        if x[node.feature_idx] <= node.threshold:
            return self._predict_sample(x, node.left)
        return self._predict_sample(x, node.right)

    def predict(self: Self, X: ndarray) -> ndarray:
        return array([self._predict_sample(x, self.tree) for x in X])


class GradientBoostingRegressor:
    """Gradient boosting regressor."""

    def __init__(
        self: Self,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
    ) -> None:
        """Initialize a gradient boosting regressor."""
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.initial_prediction = None

    def train(self: Self, x: ndarray, y: ndarray) -> None:
        """Train a gradient boosting regressor."""
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
            tree.fit(x, residuals)

            # Делаем предсказание и обновляем текущее предсказание
            pred = tree.predict(x)
            current_pred += self.learning_rate * pred
            print(f"Estimator trained {_ + 1}/{self.n_estimators}")
            # Сохраняем дерево
            self.trees.append(tree)

    def predict(self: Self, x: ndarray) -> ndarray:
        """Predict energy consumption."""
        # Начинаем с начального предсказания
        y_pred = full(x.shape[0], self.initial_prediction, dtype=float64)

        # Добавляем предсказания всех деревьев
        for tree in self.trees:
            y_pred += self.learning_rate * tree.predict(x)

        return y_pred
