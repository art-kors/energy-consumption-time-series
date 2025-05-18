import pandas as pd
import numpy as np


def extract_features(company_name):
    #TODO: создать функцию, которая возвращает pd.Dataframe() с фичами
    #пока нужно просто год, месяц, день, квартал(время года)
    #другие фичи уже уточняй уже у @AK_N0maD
    df = pd.read_csv(f'../data/{company_name}_hourly.csv')

    df['hour'] = df[f'Datetime'].apply(lambda x: pd.to_datetime(x).hour)
    df['day'] = df[f'Datetime'].apply(lambda x: pd.to_datetime(x).day)
    df['month'] = df[f'Datetime'].apply(lambda x: pd.to_datetime(x).month)
    df['year'] = df[f'Datetime'].apply(lambda x: pd.to_datetime(x).year)

    y = df[f'{company_name}_MW']
    del df[f'{company_name}_MW']
    return (df, y)





print(extract_features('AEP'))