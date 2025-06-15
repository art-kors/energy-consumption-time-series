import pandas as pd
import datetime as dt
import pickle
import numpy as np
from boosting import GradientBoostingRegressor
from nn import *


def extract_features(company_name, hour_from, hour_to, date_from, date_to):
    # TODO: создать функцию, которая возвращает pd.Dataframe() с фичами
    # пока нужно просто год, месяц, день, квартал(время года)
    # другие фичи уже уточняй уже у @AK_N0maD
    df = pd.read_csv(f"../data/{company_name}_hourly.csv")

    df['Datetime'] = pd.to_datetime(df['Datetime'])
    # Извлекаем компоненты даты и времени
    df[f'year'] = df['Datetime'].dt.year
    df[f'month'] = df['Datetime'].dt.month
    df[f'day'] = df['Datetime'].dt.day
    df[f'hour'] = df['Datetime'].dt.hour

    # Дополнительные полезные признаки
    df[f'dayofweek'] = df['Datetime'].dt.dayofweek  # 0-6 (пн-вс)
    df[f'is_weekend'] = df['Datetime'].dt.dayofweek // 5  # 1 если выходной
    df[f'quarter'] = df['Datetime'].dt.quarter
    df[f'dayofyear'] = df['Datetime'].dt.dayofyear
    df[f'weekofyear'] = df['Datetime'].dt.isocalendar().week
    print('filtration')
    df = data_filter(df, hour_from, hour_to, date_from, date_to)

    df[f'day_sin'] = np.sin(df['day'])
    df[f'day_cos'] = np.cos(df['day'])
    #del df['day']
    df[f'hour_sin'] = np.sin(df['hour'])
    df[f'hour_cos'] = np.cos(df['hour'])
    #del df['hour']
    df[f'month_sin'] = np.sin(df['month'])
    df[f'month_cos'] = np.cos(df['month'])
    #del df['month']
    y = df[f"{company_name}_MW"]
    del df[f"{company_name}_MW"]
    del df['Datetime']
    return (df, y)


def data_filter(df, hour_from, hour_to, date_from, date_to):  # date info is tuple in format (from, to)
    df = df[(df['hour'] >= hour_from) & (df['hour'] <= hour_to) &
            (df['Datetime'] >= date_from) & (df['Datetime'] <= date_to)]
    return df


def save_model(company_name, hour_from, hour_to, date_from, date_to, filename, method="Boosting"):
    X_train, y_train = extract_features(company_name, hour_from, hour_to, date_from, date_to)
    columns = X_train.columns
    X_train, y_train = X_train.to_numpy(), y_train.to_numpy()
    model = None
    if method == 'Boosting':
        model = GradientBoostingRegressor(n_estimators=50, learning_rate=0.0001, max_depth=10)
        model.fit(X_train, y_train)
    elif method == 'NeuralNetwork':
        model = NeuralNetwork([
            Dense(X_train.shape[1], X_train.shape[1]//2),
            ReLU(),
            Dense(X_train.shape[1]//2, X_train.shape[1]//4),
            ReLU(),
            Dense(X_train.shape[1]//4, 1),
            ReLU()
        ],
            loss=mse,
            loss_prime=mse_prime,
            numeric_features=[*columns])
        model.train(X_train=X_train, y_train=y_train, batch_size=128, epochs=10, learning_rate=0.01)
    else:
        raise "There is no model"
    with open(f'{filename}.pkl', 'wb') as f:
        pickle.dump(model, f)
