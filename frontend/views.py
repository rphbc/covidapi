import pytz
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import pandas as pd

# Create your views here.
from django.urls import reverse

from django.views.generic import TemplateView

from api.models import ConfirmedData, DeadData, RecoveredData, CovidData, \
    ImportsUpdate
from api.tasks import update_database
from frontend.utils import plotlinechart, curva_evolucao_confirmados, \
    plot_curva_evolucao_confirmados, progressao_confirmados, \
    plot_progressao_confirmados, acumulo_progressao_confirmados, \
    plot_acumulo_progressao_confirmados, projecao_brasil, plot_projecao_brasil, \
    plot_curva_log_confirmados_brasil, curva_log_confirmados_mundo, \
    plot_curva_log_confirmados_mundo, curva_log_confirmados_brasil, \
    trata_base_Einstein, \
    feature_importance_Einstein, predict_Einstein, predict_Einstein2, \
    triple_graph, plot_triple_graph

from .forms import NameForm

def update_graph(request):
    update_database()
    return HttpResponse('updated')


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        conf = ConfirmedData.objects.all().values('country', 'count', 'timestamp')
        dead = DeadData.objects.all().values('country', 'count',
                                             'timestamp')
        recovered = RecoveredData.objects.all().values('country', 'count', 'timestamp')

        states_data = CovidData.objects.all().values(
            'country', 'state', 'deaths', 'new_deaths', 'total_cases',
            'new_cases', 'timestamp'
        )

        last_updated = None
        try:
            last_updated = ImportsUpdate.objects.latest(
                'created_at').created_at
        except ConfirmedData.DoesNotExist:
            print('Empty database')

        df_conf = pd.DataFrame.from_records(conf, index='timestamp')
        df_dead = pd.DataFrame.from_records(dead, index='timestamp')
        df_recovered = pd.DataFrame.from_records(recovered, index='timestamp')
        df_br_states = pd.DataFrame.from_records(states_data, index='timestamp')

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

        df_plot5 = curva_log_confirmados_mundo(df_conf,lista_paises)

        plot_5 = plot_curva_log_confirmados_mundo(df_plot5,lista_paises)

        df_plot6 = curva_log_confirmados_brasil(df_br_states, [])

        plot_6 = plot_curva_log_confirmados_brasil(df_plot6, [])

        dados_graf_7 = triple_graph(df_conf, df_dead, df_recovered)

        plot_7 = plot_triple_graph(dados_graf_7)

        context.update({
            'chart_1': plot_1,
            'chart_2': plot_2,
            'chart_3': plot_3,
            'chart_4': plot_4,
            'chart_5': plot_5,
            'chart_6': plot_6,
            'chart_7': plot_7,
            'last_update': last_updated
        })

        return context


class Simulation(TemplateView):
    template_name = "simulation.html"

class Diagnose(TemplateView):
    template_name = "diagnose.html"

    def get_context_data(self, **kwargs):
        context = super(Diagnose, self).get_context_data(**kwargs)

        base = trata_base_Einstein(0)

        ft_import = feature_importance_Einstein(base)

        pred = predict_Einstein(ft_import)


        context.update({
            'top15': ft_import['top15'],
            'acuracia': pred['acuracia'],
            'modelo_ft_import': ft_import['model'],
            'modelo_mlpc': pred['param_mlpc'],
            'dados_neg': pred['dados_neg'],
            'result_neg': pred['result_neg'],
            'dados_pos': pred['dados_pos'],
            'result_pos': pred['result_pos'],
            'top15_names': ft_import['top15_names'],
        })

        return context

def vote(request):
    if request.method == "POST":
        question = request.POST.get('question_id',999)
        question2 = request.POST.get('question_id2', 999)
    return HttpResponseRedirect(reverse('frontend:result_vote',args=[question,question2]))

def result_vote(request, question_id, question_id2):

    result = int(question_id) + int(question_id2)
    return HttpResponse(str(question_id)+"  "+str(question_id2)+"   "+str(result))

def predict(request):
    if request.method == "POST":
        lista_pred=[]
        for i in range(15):
            lista_pred.append(request.POST.get('question_id'+str(i+1),999))
    return HttpResponseRedirect(reverse('frontend:result_predict',args=[lista_pred[0],lista_pred[1],lista_pred[2],
                                                                        lista_pred[3],lista_pred[4],lista_pred[5],
                                                                        lista_pred[6],lista_pred[7],lista_pred[8],
                                                                        lista_pred[9],lista_pred[10],lista_pred[11],
                                                                        lista_pred[12],lista_pred[13],lista_pred[14]]))

def result_predict(request,question_id1,question_id2,question_id3,question_id4,question_id5,
                   question_id6,question_id7,question_id8,question_id9,question_id10,
                   question_id11,question_id12,question_id13,question_id14,question_id15):

    lista_pred=[question_id1,question_id2,question_id3,question_id4,question_id5,question_id6,question_id7,
                question_id8,question_id9,question_id10,question_id11,question_id12,question_id13,
                question_id14,question_id15]

    base = trata_base_Einstein(0)

    ft_import = feature_importance_Einstein(base)

    pred = predict_Einstein2(ft_import,lista_pred)

    return HttpResponse("Seu resultado é: <strong>"+str(pred['result'])+"</strong><br>com uma precisão de: <strong>"+
                        str(pred['acuracia'])+"%</strong><br><br>Teste positivo = "+str(pred['result_pos'])+
                        "<br>Teste negativo = "+str(pred['result_neg'])+
                        "<br><br>Se os testes acima não derem POSITIVO e NEGATIVO, respectivamente, pressione "+
                        "<strong>f5</strong> para um novo treinamento da rede neural.")
