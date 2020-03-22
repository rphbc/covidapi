from django.shortcuts import render
import pandas as pd


# Create your views here.

from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        df = pd.read_csv('../time_series_19-covid-Confirmed.csv')
        df_tot = df.groupby('Country/Region').sum()
        df_tot.drop(['Lat', 'Long'], axis=1, inplace=True)
        df_tot = df_tot.T
        df_brazil = df_tot['Brazil'].loc[df_tot['Brazil'] > 50]
        df_italy = df_tot['Italy'].loc[
            (df_tot['Italy'] > 50) & (df_tot['Italy'] < df_brazil.max())]

        df_countrys = pd.DataFrame([df_brazil, df_italy]).T
        df_countrys.index = pd.to_datetime(df_countrys.index)
        df_countrys.index = df_countrys.index.strftime("%Y-%m-%d")

        context.update({'chart': plotlinechart('teste', 'teste')})

        return context