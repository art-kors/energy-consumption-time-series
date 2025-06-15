import os
import pickle
from library import functional


for filename in os.listdir('../data'):
    company = filename.split('_hourly')[0]
    print(company)
    if company+'_regressor.pkl' in os.listdir():
        continue
    functional.pickle_model(company, company+'_regressor')