import pickle

import numpy as np
import pandas as pd

from .boosting import GradientBoostingRegressor


def extract_features(company_name):
    # TODO: создать функцию, которая возвращает pd.Dataframe() с фичами
    # пока нужно просто год, месяц, день, квартал(время года)
    # другие фичи уже уточняй уже у @AK_N0maD
    df = pd.read_csv(f"../data/{company_name}_hourly.csv")

    df["Datetime"] = pd.to_datetime(df["Datetime"])
    # Извлекаем компоненты даты и времени
    df["year"] = df["Datetime"].dt.year
    df["month"] = df["Datetime"].dt.month
    df["day"] = df["Datetime"].dt.day
    df["hour"] = df["Datetime"].dt.hour

    # Дополнительные полезные признаки
    df["dayofweek"] = df["Datetime"].dt.dayofweek  # 0-6 (пн-вс)
    df["is_weekend"] = df["Datetime"].dt.dayofweek // 5  # 1 если выходной
    df["quarter"] = df["Datetime"].dt.quarter
    df["dayofyear"] = df["Datetime"].dt.dayofyear
    df["weekofyear"] = df["Datetime"].dt.isocalendar().week
    print("filtration")
    # df = data_filter(df, hour_from, hour_to, date_from, date_to)

    df["day_sin"] = np.sin(df["day"])
    df["day_cos"] = np.cos(df["day"])
    # del df['day']
    df["hour_sin"] = np.sin(df["hour"])
    df["hour_cos"] = np.cos(df["hour"])
    # del df['hour']
    df["month_sin"] = np.sin(df["month"])
    df["month_cos"] = np.cos(df["month"])
    # del df['month']
    y = df[f"{company_name}_MW"]
    del df[f"{company_name}_MW"]
    del df["Datetime"]
    return (df, y)


def generate_features(hour_from, hour_to, date_from, date_to):  # X only!
    # Создаем диапазон дат
    dates = pd.date_range(start=date_from, end=date_to, freq="D")

    # Создаем временные метки внутри указанного интервала
    time_range = pd.date_range(
        start=f"{hour_from}:00",
        end=f"{hour_to}:00",
        freq="1h",
    ).time

    # Генерируем все комбинации дат и времени
    datetime_list = []
    for date in dates:
        for time in time_range:
            datetime_list.append(
                pd.to_datetime(str(date.date()) + " " + str(time)),
            )

    df = pd.DataFrame({"Datetime": datetime_list})
    return df


def data_filter(
    df,
    hour_from,
    hour_to,
    date_from,
    date_to,
):  # date info is tuple in format (from, to)
    df = df[
        (df["hour"] >= hour_from)
        & (df["hour"] <= hour_to)
        & (df["Datetime"] >= date_from)
        & (df["Datetime"] <= date_to)
    ]
    return df


def pickle_model(company_name, filename, method="Boosting"):
    X_train, y_train = extract_features(company_name)
    columns = X_train.columns
    X_train, y_train = X_train.to_numpy(), y_train.to_numpy()
    model = None
    if method == "Boosting":
        model = GradientBoostingRegressor(
            n_estimators=50,
            learning_rate=0.0001,
            max_depth=5,
        )
        model.train(X_train, y_train)
    elif method == "NeuralNetwork":
        # TODO: in near future
        pass
    else:
        raise "There is no model"
    with open(f"{filename}.pkl", "wb") as f:
        pickle.dump(model, f)


def model_predict(filename, hour_from, hour_to, date_from, date_to):
    df = generate_features(hour_from, hour_to, date_from, date_to)
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    # Извлекаем компоненты даты и времени
    df["year"] = df["Datetime"].dt.year
    df["month"] = df["Datetime"].dt.month
    df["day"] = df["Datetime"].dt.day
    df["hour"] = df["Datetime"].dt.hour

    # Дополнительные полезные признаки
    df["dayofweek"] = df["Datetime"].dt.dayofweek  # 0-6 (пн-вс)
    df["is_weekend"] = df["Datetime"].dt.dayofweek // 5  # 1 если выходной
    df["quarter"] = df["Datetime"].dt.quarter
    df["dayofyear"] = df["Datetime"].dt.dayofyear
    df["weekofyear"] = df["Datetime"].dt.isocalendar().week

    df["day_sin"] = np.sin(df["day"])
    df["day_cos"] = np.cos(df["day"])
    # del df['day']
    df["hour_sin"] = np.sin(df["hour"])
    df["hour_cos"] = np.cos(df["hour"])
    # del df['hour']
    df["month_sin"] = np.sin(df["month"])
    df["month_cos"] = np.cos(df["month"])
    del df["Datetime"]

    X = df.to_numpy()
    model = 0
    with open(f"{filename}.pkl", "rb") as f:
        model = pickle.load(f)
    pred = model.predict(X)
    return pred


def model_predict_by_data(filename, X):
    model = 0
    with open(f"{filename}.pkl", "rb") as f:
        model = pickle.load(f)
    pred = model.predict(X)
    return pred
