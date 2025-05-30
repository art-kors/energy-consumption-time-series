import pandas as pd


def extract_features(company_name):
    # TODO: создать функцию, которая возвращает pd.Dataframe() с фичами
    # пока нужно просто год, месяц, день, квартал(время года)
    # другие фичи уже уточняй уже у @AK_N0maD
    df = pd.read_csv(f"../data/{company_name}_hourly.csv")

    df["hour"] = df["Datetime"].apply(lambda x: pd.to_datetime(x).hour)
    df["day"] = df["Datetime"].apply(lambda x: pd.to_datetime(x).day)
    df["month"] = df["Datetime"].apply(lambda x: pd.to_datetime(x).month)
    df["year"] = df["Datetime"].apply(lambda x: pd.to_datetime(x).year)

    y = df[f"{company_name}_MW"]
    del df[f"{company_name}_MW"]
    return (df, y)
