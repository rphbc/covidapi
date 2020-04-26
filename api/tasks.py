import logging
from datetime import datetime
from timeit import default_timer as timer
from io import StringIO

import pandas as pd
import pytz
import requests
from celery.schedules import crontab
from celery.task import Task

from api.models import ConfirmedData, DeadData, RecoveredData, CovidData, \
    ImportsUpdate
from covidapi.celery import app

logger = logging.getLogger('api_tasks')


class CalculateOrder(Task):

    def run(self, order_id, task_caller='checkout', *args, **kwargs):
        t0 = timer()

        t1 = timer()
        logger.info('Calculations finished in {}'.format(t1 - t0))


def save_import_log(endpoint, columns, rows_count, cols_count,
                    total_import_time):
    ImportsUpdate.objects.create(
        endpoint=endpoint,
        columns=columns,
        rows_count=rows_count,
        cols_count=cols_count,
        total_import_time=total_import_time
    )

def update_john_hopkins():
    t0 = timer()
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
    data_types = [
        'time_series_covid19_confirmed_global.csv',
        'time_series_covid19_deaths_global.csv',
        'time_series_covid19_recovered_global.csv'
    ]
    columns = ['confirmed', 'deaths', 'recovered']
    urls = [url + endpoint for endpoint in data_types]

    endpoints = zip(columns, urls)
    data = {}
    with requests.Session() as s:
        for col, endpoint in endpoints:
            data[col] = s.get(endpoint).content.decode('utf-8')

    tables = {
        'confirmed': ConfirmedData,
        'deaths': DeadData,
        'recovered': RecoveredData,
    }
    t1 = timer()
    for key, value in data.items():
        t2 = timer()
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
        tables[key].objects.bulk_create(models, batch_size=500)
        t3 = timer()
        total_execution_time = (t1-t0) + (t3-t2)
        save_import_log(
            url,
            df_tot.columns.to_list(),
            df_tot.shape[0],
            df_tot.shape[1],
            total_execution_time
        )


def update_convidbr():
    t0 = timer()
    url = 'https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv'
    with requests.Session() as s:
        data = s.get(url).content.decode('utf-8')
    data_content = StringIO(str(data))
    df = pd.read_csv(data_content)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', drop=True, inplace=True)

    data_list = []
    for idx, row in df.iterrows():
        model = CovidData()
        model.timestamp = idx.replace(tzinfo=pytz.timezone(
            'America/Sao_Paulo')).isoformat()
        model.country = row.get('country', None)
        model.state = row.get('state', None)
        model.city = row.get('city', None)
        model.ibge_id = row.get('ibgeID', None)
        model.new_deaths = row.get('newDeaths', None)
        model.deaths = row.get('deaths', None)
        model.new_cases = row.get('newCases', None)
        model.total_cases = row.get('totalCases', None)
        model.new_recovered = row.get('newRecovered', None)
        model.recovered = row.get('recovered', None)
        data_list.append(model)

    CovidData.objects.all().delete()
    CovidData.objects.bulk_create(data_list, batch_size=500)
    t1 = timer()
    total_execution_time = t1-t0
    save_import_log(
        url,
        df.columns.to_list(),
        df.shape[0],
        df.shape[1],
        total_execution_time
    )



@app.task(ignore_result=True)
def update_database():
    try:
        update_john_hopkins()
        update_convidbr()
        logger.info('Dados atualizados no banco com sucesso')
    except Exception:
        logger.exception("Import error occurred")


# Registering to the scheduler
app.add_periodic_task(crontab(minute=0, hour=8), update_database.s(),
                      name='update_scheduler',
                      )
