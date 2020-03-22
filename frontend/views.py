from django.shortcuts import render
import pandas as pd

# Create your views here.

from django.views.generic import TemplateView

from api.models import ConfirmedData, DeadData, RecoveredData
from api.tasks import update_database
from frontend.utils import plotlinechart, curva_evolucao_confirmados, \
    plot_curva_evolucao_confirmados, progressao_confirmados, \
    plot_progressao_confirmados, acumulo_progressao_confirmados, \
    plot_acumulo_progressao_confirmados, projecao_brasil, plot_projecao_brasil


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        # update_database()

        conf = ConfirmedData.objects.all().values()
        dead = DeadData.objects.all().values()
        recovered = RecoveredData.objects.all().values()

        df_conf = pd.DataFrame.from_records(conf, index='timestamp')
        df_dead = pd.DataFrame.from_records(dead, index='timestamp')
        df_recovered = pd.DataFrame.from_records(recovered, index='timestamp')

        df_conf.drop(['id'], axis=1, inplace=True)

        # plot = plotlinechart(df_conf, ['Brazil', 'Italy'], 'Confirmados')

        lista_paises = ['Australia', 'Iran', 'Italy', 'Japan', 'Korea, South',
                        'Spain', 'United Kingdom', 'US', 'Netherlands',
                        'Norway', 'Brazil', 'China']

        lista_paises2 = ['Italy', 'China', 'Korea, South']

        dados_paises = pd.DataFrame(data={
            'Country/Region': ['Australia', 'Brazil', 'Iran', 'Italy', 'Japan',
                               'Korea, South', 'Netherlands', 'Norway',
                               'Spain', 'US', 'United Kingdom', 'China'],
            'Color': ['rgb(67, 207, 246)', 'rgb(255, 90, 67)',
                      'rgb(230, 220, 215)', 'rgb(230, 220, 215)',
                      'rgb(230, 220, 215)', 'rgb(230, 220, 215)',
                      'rgb(255, 142, 46)', 'rgb(0, 151, 150)',
                      'rgb(230, 220, 215)', 'rgb(153, 213, 213)',
                      'rgb(230, 220, 215)', 'rgb(114,34,130)'],
            'Width': [4, 4, 2, 2, 2, 2, 4, 4, 2, 4, 2, 4],
            'Order': [11, 12, 1, 2, 3, 4, 8, 9, 6, 7, 5, 10]})

        dados_graf_1 = curva_evolucao_confirmados(df_conf, lista_paises)

        plot_1 = plot_curva_evolucao_confirmados(dados_graf_1, dados_paises,
                                                 plot_china=1)

        dados_graf_2 = progressao_confirmados(df_conf, lista_paises)

        plot_2 = plot_progressao_confirmados(dados_graf_2, dados_paises, 1)

        dados_graf_3 = acumulo_progressao_confirmados(df_conf, lista_paises)

        plot_3 = plot_acumulo_progressao_confirmados(dados_graf_3,
                                                     dados_paises, 1)

        dados_graf_4 = projecao_brasil(df_conf, lista_paises, lista_paises2)

        plot_4 = plot_projecao_brasil(dados_graf_4, dados_paises, 1)

        context.update({
            'chart_1': plot_1,
            'chart_2': plot_2,
            'chart_3': plot_3,
            'chart_4': plot_4,
        })

        return context
