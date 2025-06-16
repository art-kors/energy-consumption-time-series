"""ML functional module."""

import pickle
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from numpy import cos, ndarray, sin
from pandas import DataFrame, concat, date_range

from .boosting import GradientBoostingRegressor


def extract_features(company_name: str) -> tuple[ndarray, ndarray]:
    """Extract features for model training."""
    data_frame = pd.read_csv(f"./data/companies/{company_name}_hourly.csv")

    data_frame["Datetime"] = pd.to_datetime(data_frame["Datetime"])
    # Извлекаем компоненты даты и времени
    data_frame["year"] = data_frame["Datetime"].dt.year
    data_frame["month"] = data_frame["Datetime"].dt.month
    data_frame["day"] = data_frame["Datetime"].dt.day
    data_frame["hour"] = data_frame["Datetime"].dt.hour

    # Дополнительные полезные признаки
    data_frame["dayofweek"] = data_frame[
        "Datetime"
    ].dt.dayofweek  # 0-6 (пн-вс)
    data_frame["is_weekend"] = (
        data_frame["Datetime"].dt.dayofweek // 5
    )  # 1 если выходной
    data_frame["quarter"] = data_frame["Datetime"].dt.quarter
    data_frame["dayofyear"] = data_frame["Datetime"].dt.dayofyear
    data_frame["weekofyear"] = data_frame["Datetime"].dt.isocalendar().week

    data_frame["day_sin"] = np.sin(data_frame["day"])
    data_frame["day_cos"] = np.cos(data_frame["day"])
    data_frame["hour_sin"] = np.sin(data_frame["hour"])
    data_frame["hour_cos"] = np.cos(data_frame["hour"])
    data_frame["month_sin"] = np.sin(data_frame["month"])
    data_frame["month_cos"] = np.cos(data_frame["month"])

    y = data_frame[f"{company_name}_MW"]
    del data_frame[f"{company_name}_MW"]
    del data_frame["Datetime"]
    return data_frame.to_numpy(), y.to_numpy()


def generate_features(start: datetime, end: datetime) -> DataFrame:  # X only!
    """Create date range."""
    return DataFrame({"Datetime": date_range(start=start, end=end, freq="1h")})


def pickle_model(company_name: str) -> None:
    """Train model on dataset and pickle it."""
    x_train, y_train = extract_features(company_name)
    model = GradientBoostingRegressor(
        n_estimators=50,
        learning_rate=0.0001,
        max_depth=5,
    )
    model.train(x_train, y_train)
    with Path(f"./data/models/{company_name}_regressor.pkl").open(
        mode="wb",
    ) as file:
        pickle.dump(model, file)


def model_predict(
    company_name: str,
    start: datetime,
    end: datetime,
) -> DataFrame:
    """Predict energy consumption."""
    data_frame = generate_features(start, end)
    data_frame["Datetime"] = pd.to_datetime(data_frame["Datetime"])

    # Извлекаем компоненты даты и времени
    data_frame["year"] = data_frame["Datetime"].dt.year
    data_frame["month"] = data_frame["Datetime"].dt.month
    data_frame["day"] = data_frame["Datetime"].dt.day
    data_frame["hour"] = data_frame["Datetime"].dt.hour

    # Дополнительные полезные признаки
    data_frame["dayofweek"] = data_frame[
        "Datetime"
    ].dt.dayofweek  # 0-6 (пн-вс)
    data_frame["is_weekend"] = (
        data_frame["Datetime"].dt.dayofweek >= 5
    )  # 1 если выходной
    data_frame["quarter"] = data_frame["Datetime"].dt.quarter
    data_frame["dayofyear"] = data_frame["Datetime"].dt.dayofyear
    data_frame["weekofyear"] = data_frame["Datetime"].dt.isocalendar().week

    data_frame["day_sin"] = sin(data_frame["day"])
    data_frame["day_cos"] = cos(data_frame["day"])

    data_frame["hour_sin"] = sin(data_frame["hour"])
    data_frame["hour_cos"] = cos(data_frame["hour"])

    data_frame["month_sin"] = sin(data_frame["month"])
    data_frame["month_cos"] = cos(data_frame["month"])

    saved = data_frame["Datetime"]
    del data_frame["Datetime"]

    x = data_frame.to_numpy()
    model = 0
    with Path(f"./data/models/{company_name}_regressor.pkl").open(
        mode="rb",
    ) as file:
        model = pickle.load(file)
    pred = DataFrame({f"{company_name}_MW": model.predict(x)})
    return concat([saved, data_frame, pred], axis=1)
