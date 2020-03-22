import logging
from timeit import default_timer as timer
from io import StringIO

import pandas as pd
import requests
from celery.task import Task

from api.models import ConfirmedData, DeadData, RecoveredData
from covidapi.celery import app

logger = logging.getLogger('api_tasks')


class CalculateOrder(Task):

    def run(self, order_id, task_caller='checkout', *args, **kwargs):
        t0 = timer()

        t1 = timer()
        logger.info('Calculations finished in {}'.format(t1 - t0))


@app.task(ignore_result=True)
def update_database():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
    data_types = [
        'time_series_19-covid-Confirmed.csv',
        'time_series_19-covid-Deaths.csv',
        'time_series_19-covid-Recovered.csv'
    ]
    columns = ['confirmed', 'deaths', 'recovered']
    urls = [url + endpoint for endpoint in data_types]

    endpoints = zip(columns, urls)
    data = {}
    with requests.Session() as s:
        for col, endpoint in endpoints:
            data[col] = s.get(endpoint).content.decode('utf-8')

    print(data)

    tables = {
        'confirmed': ConfirmedData,
        'deaths': DeadData,
        'recovered': RecoveredData,
    }

    for key, value in data.items():
        data_content = StringIO(str(value))
        df = pd.read_csv(data_content)
        df_tot = df.groupby('Country/Region').sum()
        df_tot.drop(['Lat', 'Long'], axis=1, inplace=True)
        df_tot = df_tot.T
        df_tot.index = pd.to_datetime(df_tot.index)

        models = []
        for idx, row in df_tot.iterrows():

            timestamp = idx
            for country, value in row.items():
                model = tables[key]()
                model.count = value
                model.timestamp = timestamp
                model.country = country
                models.append(model)

        tables[key].objects.all().delete()
        tables[key].objects.bulk_create(models, batch_size=100)
        logger.info('Dados atualizados no banco com sucesso')


# Registering to the scheduler
app.add_periodic_task(20.0, update_database.s(), name='update_scheduler',
                      expires=60.0)
