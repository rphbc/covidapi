import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import ExtraTreesClassifier

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import openpyxl

from timeit import default_timer as timer


def plotlinechart(data_list, countries, plot_name):
    data_list.index = data_list.index.strftime("%Y-%m-%d")

    fig = go.Figure()

    if not countries:
        countries = data_list['country'].unique()

    for country in countries:
        df = data_list['count'].loc[data_list['country'] == country]
        x = df.index
        values = df.values
        fig.add_trace(go.Scatter(
            x=x,
            y=values,
            name=country,  # Style name/legend entry with html tags
            connectgaps=True  # override default to connect the gaps
        ))
    fig.update_layout(yaxis_type="log")
    chart = py.plot(
        fig,
        show_link=False,
        output_type='div',
        include_plotlyjs=False,
        auto_open=False,
    )

    return chart


def curva_log_confirmados_mundo(df_hist,lista_paises):

    # dt0 = timer()

    country_list = list(df_hist['country'].unique())
    country_dict = {country: df_hist.loc[df_hist['country'] == country] for
                    country in
                    country_list}
    country_dict2 = []
    resample_freq = '2D'
    for country, df in country_dict.items():
        df2 = df.loc[df['count'] > 50]  # Cut the begining of the curve
        df2 = df2.resample(resample_freq).mean()
        df2['new_cases'] = np.round(df2['count'] - df2['count'].shift(1))
        df2['country'] = country
        df2.fillna(0.0, inplace=True)
        country_dict2.append(df2)

    df_tot = pd.concat(country_dict2)
    df_tot.reset_index(inplace=True)
    df_tot.rename(columns={'count': 'acumulated'}, inplace=True)
    # dt1 = timer()
    # create a column of acumulated cases
    # df_hist['new_cases'] = 0
    # df_hist = df_hist.sort_values(by=['country', 'timestamp'])
    #
    # # rename the 'count' column to "new_cases"
    # df_hist = df_hist.rename(columns={'count': 'acumulated'})
    #
    # # reset index
    # df_hist = df_hist.reset_index()
    #
    # # iterate to sum acumulated cases
    # for index, row in df_hist.iterrows():
    #
    #     if index != 0:
    #         if df_hist.iloc[index - 1]['country'] == df_hist.iloc[index]['country']:
    #             df_hist.at[index, 'new_cases'] = df_hist.iloc[index]['acumulated'] - df_hist.iloc[index - 1][
    #                 'acumulated']
    #         else:
    #             pass
    # dt2 = timer()

    # print(f' tempo um : {dt1-dt0}')
    # print(f'tempo dois: {dt2-dt1}')
    # return df_hist
    return df_tot


def plot_curva_log_confirmados_mundo(df_hist, lista_paises):

    fig = go.Figure()

    for l in lista_paises:
        fig.add_trace(go.Scatter(name=str(l), x=df_hist.groupby('country').get_group(str(l))['acumulated'],
                                 y=df_hist.groupby('country').get_group(str(l))['new_cases']))

    fig.update_layout(yaxis_type="log", xaxis_type="log", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',title='Casos totais x casos novos Mundo')

    fig.update_xaxes(title_text='total de casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')
    fig.update_yaxes(title_text='novos casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')

    chart = py.plot(
        fig,
        show_link=False,
        output_type='div',
        include_plotlyjs=False,
        auto_open=False,
    )

    return chart


def curva_log_confirmados_brasil(df_hist, lista_estados):


    ################################################################################################
    # upload csv
    csv = 'covid_br_state.csv'
    df_hist = pd.read_csv(csv, sep=';|,')

    # order data to ensure chronology
    df_hist.timestamp = pd.to_datetime(df_hist.timestamp)
    df_hist = df_hist.sort_values(by=['country', 'timestamp'])
    ################################################################################################

    # create a column of acumulated cases
    df_hist['new_cases'] = 0

    # rename the 'count' column to "new_cases"
    df_hist = df_hist.rename(columns={'count': 'acumulated'})

    # reset index
    df_hist = df_hist.reset_index()

    # iterate to sum acumulated cases
    for index, row in df_hist.iterrows():

        if index != 0:
            if df_hist.iloc[index - 1]['country'] == df_hist.iloc[index]['country']:
                df_hist.at[index, 'new_cases'] = df_hist.iloc[index]['acumulated'] - df_hist.iloc[index - 1][
                    'acumulated']
            else:
                continue

    return df_hist


def plot_curva_log_confirmados_brasil(df_hist, lista_estados):

    fig = go.Figure()

    # fig.add_trace(go.Scatter(name="SP",x=df_hist.groupby('country').get_group('SP')['acumulated'],y=df_hist.groupby('country').get_group('SP')['new_cases']))
    # fig.add_trace(go.Scatter(name="RJ",x=df_hist.groupby('country').get_group('RJ')['acumulated'],y=df_hist.groupby('country').get_group('RJ')['new_cases']))
    # fig.add_trace(go.Scatter(name="DF",x=df_hist.groupby('country').get_group('DF')['acumulated'],y=df_hist.groupby('country').get_group('DF')['new_cases']))

    for i in list(df_hist['country'].unique()):
        fig.add_trace(go.Scatter(x=list(df_hist.loc[df_hist['country']==i,'acumulated']),
                             y=list(df_hist.loc[df_hist['country']==i,'new_cases']), name=i,mode='lines'))

    fig.update_layout(yaxis_type="log", xaxis_type="log", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',title='Casos totais x casos novos BR')

    fig.update_xaxes(title_text='total de casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')
    fig.update_yaxes(title_text='novos casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')

    chart = py.plot(
        fig,
        show_link=False,
        output_type='div',
        include_plotlyjs=False,
        auto_open=False,
    )

    return chart


def curva_evolucao_confirmados(base,lista_paises):
        confirmed_cases_t2 = base.reset_index()
        confirmed_cases_t2.columns = ['variable','Country/Region','value']
        first_date = confirmed_cases_t2.loc[confirmed_cases_t2['value']>=50].sort_values(by=['Country/Region','variable']).groupby('Country/Region').head(1)
        first_date = first_date[['Country/Region', 'variable']]
        first_date.columns = ['Country/Region', 'first_date']
        confirmed_cases_t3 = confirmed_cases_t2.merge(first_date,on='Country/Region', how='left')
        confirmed_cases_t4 = confirmed_cases_t3.loc[~confirmed_cases_t3['first_date'].isna()]
        confirmed_cases_t4['var_dates'] = (confirmed_cases_t4['variable'] - confirmed_cases_t4['first_date']).dt.days
        confirmed_cases_t5 = confirmed_cases_t4.loc[confirmed_cases_t4['var_dates']>=0].sort_values(by=['Country/Region','var_dates']).groupby(['Country/Region','var_dates']).agg({'value':sum}).reset_index()
        paises_show = confirmed_cases_t5.groupby('Country/Region')['var_dates'].count().reset_index()
        confirmed_cases_t5 = confirmed_cases_t5.loc[confirmed_cases_t5['Country/Region'].isin(list(paises_show.loc[paises_show['var_dates']>=5,'Country/Region']))]
        confirmed_cases_t6 = confirmed_cases_t5.loc[confirmed_cases_t5['Country/Region'].isin(lista_paises)]
        curva_evolucao_confirmados = confirmed_cases_t6
        return curva_evolucao_confirmados

def plot_curva_evolucao_confirmados(dados_graf,dados_paises,plot_china=0):
    fig = go.Figure()

    dados_graf = dados_graf.merge(dados_paises[['Country/Region','Order']].drop_duplicates(),on='Country/Region').sort_values(by=['Order','var_dates'])

    dados_graf = dados_graf.loc[dados_graf['var_dates']<=dados_graf.loc[dados_graf['Country/Region']!='China','var_dates'].max()]

    if plot_china==0:
        dados_graf = dados_graf.loc[~dados_graf['Country/Region'].isin(['China'])]

    for i in list(dados_graf['Country/Region'].unique()):
        fig.add_trace(go.Scatter(x=list(dados_graf.loc[dados_graf['Country/Region']==i,'var_dates']),
                             y=list(dados_graf.loc[dados_graf['Country/Region']==i,'value']), name=i,mode='lines',line_shape='spline',
                             line=dict(color=dados_paises.loc[dados_paises['Country/Region']==i,'Color'].values[0],width=dados_paises.loc[dados_paises['Country/Region']==i,'Width'].values[0])))

    fig.update_layout(yaxis_type="log",paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',title='Evolução de casos confirmados para países selecionados')

    fig.update_xaxes(title_text='# Dias desde a confirmação de 50 casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')
    fig.update_yaxes(title_text='# casos (k)', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')

    chart = py.plot(
        fig,
        show_link=False,
        output_type='div',
        include_plotlyjs=False,
        auto_open=False,
    )

    return chart

def progressao_confirmados(base,lista_paises):

        base_analise = curva_evolucao_confirmados(base,lista_paises)

        base_agrega = pd.DataFrame()

        for j in list(base_analise['Country/Region'].unique()):
            base_pais = base_analise.loc[base_analise['Country/Region']==j].sort_values(by='var_dates')
            for i in list(base_pais['var_dates']):
                try:
                    qtde_dias = int(base_pais.loc[base_pais['value']>=int(base_pais.loc[base_pais['var_dates']==i,'value'])*2].head(1)['var_dates'])-i
                except:
                    qtde_dias = np.nan
                base_valores = pd.DataFrame(data={'pais':j,'data':i,'qtde_dias':qtde_dias},index={0})
                base_agrega = pd.concat([base_agrega,base_valores])

        base_agrega = base_agrega.reset_index(drop=True)

        base_agrega = base_agrega.loc[~base_agrega['qtde_dias'].isna()]

        base_agrega.rename(columns={'pais':'Country/Region','data':'var_dates','qtde_dias':'value'},inplace=True)

        base_agrega = base_agrega.loc[base_agrega['Country/Region'].isin(lista_paises)]

        return base_agrega

def plot_progressao_confirmados(dados_graf,dados_paises,plot_china=0):
    fig = go.Figure()

    dados_graf = dados_graf.merge(dados_paises[['Country/Region','Order']].drop_duplicates(),on='Country/Region').sort_values(by=['Order','var_dates'])

    if plot_china==0:
        dados_graf = dados_graf.loc[~dados_graf['Country/Region'].isin(['China'])]

    for i in list(dados_graf['Country/Region'].unique()):
        fig.add_trace(go.Scatter(x=list(dados_graf.loc[dados_graf['Country/Region']==i,'var_dates']),
                             y=list(dados_graf.loc[dados_graf['Country/Region']==i,'value']), name=i,mode='lines',line_shape='spline',
                             line=dict(color=dados_paises.loc[dados_paises['Country/Region']==i,'Color'].values[0],width=dados_paises.loc[dados_paises['Country/Region']==i,'Width'].values[0])))

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title='Variação da velocidade de progressão de contaminação para países selecionados')

    fig.update_xaxes(title_text='# Dias desde a confirmação de 50 casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')
    fig.update_yaxes(title_text='# dias para dobrar número de casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')

    chart = py.plot(
            fig,
            show_link=False,
            output_type='div',
            include_plotlyjs=False,
            auto_open=False,
        )

    return chart

def acumulo_progressao_confirmados(base,lista_paises):

    base_analise = curva_evolucao_confirmados(base,lista_paises)

    m = int((5 * round(base_analise['var_dates'].max()/5))/5) + 1

    dias = [0] + list(range(5, (m * 5)+1, 5))

    base_análise_2 = base_analise.loc[base_analise['var_dates'].isin(dias)]

    base_analise_3 = base_análise_2.pivot(index='Country/Region',columns='var_dates',values='value')

    base_analise_3.columns = ['casos_'+str(i) for i in list(base_analise_3.columns)]

    cols_antes = len(base_analise_3.columns)

    for i in range(0,len(list(base_analise_3.columns))):
        #base_analise_3[list(base_analise_3.columns)[i+1] + '_' + str(dias[i])] = base_analise_3.iloc[:,i+1] / base_analise_3.iloc[:,i]
        base_analise_3[str(dias[i+1])] = base_analise_3.iloc[:,i+1] / base_analise_3.iloc[:,i]

    #base_analise_3['0'] = 1

    base_analise_3 = base_analise_3[list(base_analise_3.columns[cols_antes:])].reset_index().melt(id_vars=['Country/Region'])

    base_analise_3['variable'] = base_analise_3['variable'].astype(int)

    base_analise_3 = base_analise_3.sort_values(by=['Country/Region','variable'])

    base_analise_3['value'] = base_analise_3['value'].fillna(0)

    base_analise_3 = base_analise_3.groupby(by=['Country/Region','variable']).sum().groupby(level=[0]).cumprod().reset_index()

    maximo_valor = base_analise_3.groupby('Country/Region')['value'].max().reset_index()

    maximo_valor.rename(columns={'value':'value_max'},inplace=True)

    aux_max = base_analise_3.merge(maximo_valor,on='Country/Region',how='left')

    aux_max1 = aux_max.loc[(aux_max['value']<aux_max['value_max'])&(aux_max['value']!=0)]

    aux_max2 = aux_max.loc[aux_max['value']>=aux_max['value_max']]

    base_analise_4 = pd.concat([aux_max1,aux_max2.groupby('Country/Region').head(1)]).sort_values(by=['Country/Region','variable'])

    base_analise_4.drop(columns='value_max',inplace=True)

    coloca_zero = pd.DataFrame(data={'Country/Region':list(base_analise_4['Country/Region'].unique())})

    coloca_zero['variable'] = 0
    coloca_zero['value'] = 1

    base_analise_4 = pd.concat([base_analise_4,coloca_zero])

    base_analise_4 = base_analise_4.sort_values(by=['Country/Region','variable'])

    base_analise_4.columns = ['Country/Region', 'var_dates', 'value']

    return base_analise_4

def plot_acumulo_progressao_confirmados(dados_graf,dados_paises,plot_china=0):
    fig = go.Figure()

    dados_graf = dados_graf.merge(dados_paises[['Country/Region','Order']].drop_duplicates(),on='Country/Region').sort_values(by=['Order','var_dates'])

    dados_graf = dados_graf.loc[dados_graf['var_dates']<=dados_graf.loc[dados_graf['Country/Region']!='China','var_dates'].max()]

    if plot_china==0:
        dados_graf = dados_graf.loc[~dados_graf['Country/Region'].isin(['China'])]

    for i in list(dados_graf['Country/Region'].unique()):
        fig.add_trace(go.Scatter(x=list(dados_graf.loc[dados_graf['Country/Region']==i,'var_dates']),
                             y=list(dados_graf.loc[dados_graf['Country/Region']==i,'value']), name=i,mode='lines',line_shape='spline',
                             line=dict(color=dados_paises.loc[dados_paises['Country/Region']==i,'Color'].values[0],width=dados_paises.loc[dados_paises['Country/Region']==i,'Width'].values[0])))

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title='Progressão acumulada de contaminação em relação ao ponto 0 para países selecionados')

    fig.update_xaxes(title_text='# Dias desde a confirmação de 50 casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')
    fig.update_yaxes(title_text='Número de vezes em relação ao ponto 0, acumulado', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')

    chart = py.plot(
            fig,
            show_link=False,
            output_type='div',
            include_plotlyjs=False,
            auto_open=False,
        )

    return chart

def projecao_brasil(base,lista_paises,lista_paises2):
    base_analise = curva_evolucao_confirmados(base,lista_paises)
    base_acumulo = acumulo_progressao_confirmados(base,lista_paises)

    real_brasil = base_analise.loc[base_analise['Country/Region']=='Brazil']

    base_acumulo = base_acumulo.loc[base_acumulo['Country/Region'].isin(['Brazil']+lista_paises2)]

    aux_acumulo = base_acumulo.pivot(index='var_dates',columns='Country/Region',values='value').reset_index()

    lista_pontos = list(aux_acumulo['var_dates'].unique())

    ponteiro = [i for i,x in enumerate(lista_pontos) if x == aux_acumulo.loc[aux_acumulo['Brazil'].isna()].head(1)['var_dates'].values[0]][0]

    aux_ajusta_previsao = base_acumulo.loc[base_acumulo['var_dates']==(lista_pontos[ponteiro-1]),['Country/Region','value']]

    aux_ajusta_previsao.columns=['Country/Region','value_ajust']

    base_acumulo_2 = base_acumulo.merge(aux_ajusta_previsao,on=['Country/Region'])

    base_acumulo_2['value_new'] = base_acumulo_2['value']/base_acumulo_2['value_ajust']

    base_projecao = real_brasil.loc[real_brasil['var_dates']==lista_pontos[ponteiro-1],'value']

    base_acumulo_2['casos_projecao'] = base_acumulo_2['value_new'] * int(base_projecao)

    base_acumulo_3 = base_acumulo_2.pivot(index='var_dates',columns='Country/Region',values='casos_projecao').reset_index()

    base_acumulo_3 = base_acumulo_3.loc[base_acumulo_3['var_dates']<=30]

    aux_final = pd.DataFrame(pd.concat([base_acumulo_3[['var_dates']],real_brasil[['var_dates']]])['var_dates'].unique())

    aux_final.columns=['var_dates']

    aux_final = aux_final.sort_values(by='var_dates').merge(base_acumulo_3[['var_dates']+lista_paises2],on='var_dates',how='left').merge(real_brasil[['var_dates','value']],on='var_dates',how='left')

    aux_final.rename(columns={'value':'Brazil'},inplace=True)

    aux_final.loc[aux_final['var_dates']<lista_pontos[ponteiro-1],lista_paises2]= np.nan

    aux_final = aux_final.melt(id_vars='var_dates')[['variable','var_dates','value']]

    aux_final.rename(columns={'variable':'Country/Region'},inplace=True)

    return aux_final

def plot_projecao_brasil(dados_graf,dados_paises,plot_china=0):
    fig = go.Figure()

    dados_graf = dados_graf.merge(dados_paises[['Country/Region','Order']].drop_duplicates(),on='Country/Region').sort_values(by=['Order','var_dates'])

    dados_graf = dados_graf.loc[dados_graf['var_dates']<=dados_graf.loc[dados_graf['Country/Region']!='China','var_dates'].max()]

    if plot_china==0:
        dados_graf = dados_graf.loc[~dados_graf['Country/Region'].isin(['China'])]

    for i in list(dados_graf['Country/Region'].unique()):
        fig.add_trace(go.Scatter(x=list(dados_graf.loc[dados_graf['Country/Region']==i,'var_dates']),
                             y=list(dados_graf.loc[dados_graf['Country/Region']==i,'value']), name=i,mode='lines',line_shape='spline',
                             line=dict(color=dados_paises.loc[dados_paises['Country/Region']==i,'Color'].values[0],width=dados_paises.loc[dados_paises['Country/Region']==i,'Width'].values[0])))

    fig.update_layout(yaxis_type="log", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title='Estimativa de casos Brasil com base na taxa de progressão da contaminação de outros países')

    fig.update_xaxes(title_text='# Dias desde a confirmação de 50 casos', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')
    fig.update_yaxes(title_text='# casos (k)', showline=True, linewidth=1, linecolor='rgb(128,128,128)',showgrid=True, gridwidth=0.5, gridcolor='rgb(240,240,240)')

    chart = py.plot(
            fig,
            show_link=False,
            output_type='div',
            include_plotlyjs=False,
            auto_open=False,
        )

    return chart

class MultiColumnLabelEncoder:

    def __init__(self, columns=None):
        self.columns = columns  # list of column to encode

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''

        output = X.copy()
        #         if self.columns.dtype != 'float64':

        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname, col in output.iteritems():
                if output[colname].dtype != 'float64' and output[colname].dtype != 'datetime64[ns]':
                    output[colname] = LabelEncoder().fit_transform(col)

        return output

    def fit_transform2(self, X, y=None):
        return self.fit(X, y).transform(X)

def trata_base_Einstein(df):

    ##################################################################################3
    # upload da planilha
    excel_file = 'dataset.xlsx'

    # dataframe completo
    df = pd.read_excel(excel_file, sheet_name="All")
    ##################################################################################3

    df1 = df

    # checa se existem strings e numeros misturados
    for column in df1:
        a = list(df1[column].map(type) != str)
        if (len(set(a)) != 1):
            # converte colunas mistas para tipo string
            df1[column] = df1[column].apply(str)

    # checa se deu tudo certo
    for column in df1:
        a = list(df1[column].map(type) != str)
        # if (len(set(a)) != 1):
        #     print("valores mistos remanescentes em: " + column)

    ### como, neste caso, o timestamp não importa, pode-se preencher com qualquer valor sequencial ###

    # pega a quantidade de linhas
    qtde_linhas = len(df1.index)
    # cria uma coluna de Timestamps sequenciais na primeira posição
    df1.insert(0, "Timestamp", pd.date_range(start='1/1/2020', periods=qtde_linhas, freq='H'))

    # pega o nome das colunas
    colunas = list(df1)

    # remove colunas que não possuem nenhum dado
    df1 = df1.dropna(axis=1, how='all')

    # remove linhas sem exames sanguíneos (vi que quem não fez a de Hematocrit, não fez mais nenhum)
    df1 = df1[df1['Hematocrit'].notna()]

    # preenche espaços vazios restantes (NaN) com zeros
    df1 = df1.fillna(0)

    # transformando dados categóricos em números - exemplo: [normal,ausente,presente] viram [0,1,2]
    le = MultiColumnLabelEncoder()
    df1 = le.fit_transform2(df1)

    # definindo colunas de saida e transformando em números (neg=0 e pos=1)
    lista_out = ['Timestamp', 'SARS-Cov-2 exam result', 'Patient addmited to regular ward (1=yes, 0=no)',
                 'Patient addmited to semi-intensive unit (1=yes, 0=no)',
                 'Patient addmited to intensive care unit (1=yes, 0=no)']
    df_out = df1[lista_out]
    # df_out = df_out.replace(['negative','positive'],[0,1])
    lista_out.remove('Timestamp')

    # removendo colunas que não serão úteis para a análise e também a coluna de saída
    lista_drop = lista_out
    lista_drop.append('Patient ID')
    df1 = df1.drop(lista_drop, axis=1)
    colunas = list(df1)

    # cria o dataframe que virará o xls para subir no B-Zek
    # salva em uma nova planilha de resultados
    writer = pd.ExcelWriter('base_relevance.xlsx', engine='openpyxl')
    df1.to_excel(writer, sheet_name="INPUTS")
    df_out.to_excel(writer, sheet_name="OUTPUTS")
    writer.save()

    response = {
        'inputs':df1,
        'outputs':df_out
    }

    return response

def feature_importance_Einstein(base):

    df1 = base['inputs']
    df_out = base['outputs']

    try:
        df_out = df_out.drop(columns=['Timestamp'])
        df1 = df1.drop(columns=['Timestamp'])
    except:
        pass

    # Encontra as variáveis mais relevante para a incidência de COVID-19
    model = ExtraTreesClassifier(verbose=False)
    a = model.fit(df1, df_out)

    lista_importances = pd.DataFrame([model.feature_importances_])
    lista_importances.columns = list(df1.columns)
    lista_importances = lista_importances * 100

    lista_importances = lista_importances.sort_values(by=0, axis=1, ascending=False)

    top15 = list(lista_importances.columns[0:15])
    top15_values = []
    # print("Variáveis mais impactantes:")
    for l in lista_importances.columns[0:15]:
        # print("Nome: " + str(l) + " - " + str(lista_importances[l][0]) + " %")
        top15_values.append(lista_importances[l][0])
    # print(top15)

    # cria dataset para predição
    df_in = df1[top15]
    df_out = df_out

    # pega a lista das variáveis mais relevantes e cria outra planilha para a rede neural
    lista_neural_in = df_in
    lista_neural_out = df_out

    ### como, neste caso, o timestamp não importa, pode-se preencher com qualquer valor sequencial ###
    # pega a quantidade de linhas
    qtde_linhas = len(lista_neural_in.index)
    # cria uma coluna de Timestamps sequenciais na primeira posição
    lista_neural_in.insert(0, "Timestamp", pd.date_range(start='1/1/2020', periods=qtde_linhas, freq='H'))
    lista_neural_out.insert(0, "Timestamp", pd.date_range(start='1/1/2020', periods=qtde_linhas, freq='H'))

    df2_in = lista_neural_in.copy()
    df2_out = lista_neural_out.copy()
    writer = pd.ExcelWriter('base_simulate.xlsx', engine='openpyxl')
    lista_neural_in.to_excel(writer, sheet_name="INPUTS")
    lista_neural_out.to_excel(writer, sheet_name="OUTPUTS")
    writer.save()

    top15_aws = zip(top15, top15_values)

    response = {
        'top15' : top15_aws,
        'top15_names' : top15,
        'df_in' : df2_in,
        'df_out': df2_out,
        'model' : model.get_params(),
    }

    return response

def predict_Einstein(base):

    df_in = base['df_in']
    df_out = base['df_out']


    y = df_out['SARS-Cov-2 exam result']
    x = df_in.drop(['Timestamp'], axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=27)

    clf = MLPClassifier(hidden_layer_sizes=(100, 100, 100), max_iter=2500, alpha=0.0001,
                        solver='lbfgs', verbose=False, random_state=21,
                        tol=0.000000001)

    a = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    acc = accuracy_score(y_test, y_pred)
    acc = acc * 100
    acc = "{:.2f}".format(acc)
    # print("teste finalizado")
    # print("Acurácia = " + str(acc) + "%")

    # teste negativo
    lista_neg = [[-1.73367476463318,-1.77359390258789,0.609156608581543,1.38181185722351,17,
                  -3.2425479888916,-0.582671403884888,-0.448159873485565,-3.31828498840332,-1.83095347881317,
                  0.470262199640274,-2.77920341491699,1.55254781246185,0,2.05995225906372]]

    lista_user = lista_neg
    lista_predict = pd.DataFrame(lista_user)
    lista_predict.columns = list(x.columns)
    # print(lista_predict)

    y_pred = clf.predict(lista_predict)
    if y_pred == 0:
        result_neg = 'NEGATIVO'
    else:
        result_neg = 'POSITIVO'

    # print("Resultado: " + result_neg)

    # teste positivo
    lista_pos = [[-1.28842806816101,-0.906829118728638,-0.503570020198822,0.567652404308319,19,
                  0.69428688287735,-0.835507690906525,-0.182790279388428,0.578023791313171,-0.295725524425507,
                  -0.735871851444244,0.541563928127289,0.38068476319313,0.420203506946564,-0.135454878211021]]

    lista_user = lista_pos
    lista_predict = pd.DataFrame(lista_user)
    lista_predict.columns = list(x.columns)
    # print(lista_predict)

    y_pred = clf.predict(lista_predict)
    if y_pred == 0:
        result_pos = 'NEGATIVO'
    else:
        result_pos = 'POSITIVO'

    # print("Resultado: " + result_pos)

    params = clf.get_params()

    response = {
        'acuracia' : acc,
        'dados_neg'  : lista_neg,
        'result_neg' : result_neg,
        'dados_pos'  : lista_pos,
        'result_pos' : result_pos,
        'param_mlpc' : params,

    }

    return response

def predict_Einstein2(base,lista_pred):

    df_in = base['df_in']
    df_out = base['df_out']


    y = df_out['SARS-Cov-2 exam result']
    x = df_in.drop(['Timestamp'], axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=27)

    clf = MLPClassifier(hidden_layer_sizes=(100, 100, 100), max_iter=2500, alpha=0.0001,
                        solver='lbfgs', verbose=False, random_state=21,
                        tol=0.000000001)

    a = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    acc = accuracy_score(y_test, y_pred)
    acc = acc * 100
    acc = "{:.2f}".format(acc)
    # print("teste finalizado")
    # print("Acurácia = " + str(acc) + "%")
    #
    # print("digite os numeros em sequência:")
    lista_user = lista_pred

    lista_user = [lista_user]
    lista_predict = pd.DataFrame(lista_user)
    lista_predict.columns = list(x.columns)
    # print(lista_predict)

    y_pred = clf.predict(lista_predict)
    if y_pred == 0:
        result = 'NEGATIVO'
    else:
        result = 'POSITIVO'

    # print("********************************************************")
    # print("Resultado: " + result)
    # print("********************************************************")

    # teste negativo
    lista_neg = [[-1.73367476463318,-1.77359390258789,0.609156608581543,1.38181185722351,17,
                  -3.2425479888916,-0.582671403884888,-0.448159873485565,-3.31828498840332,-1.83095347881317,
                  0.470262199640274,-2.77920341491699,1.55254781246185,0,2.05995225906372]]

    lista_user = lista_neg
    lista_predict = pd.DataFrame(lista_user)
    lista_predict.columns = list(x.columns)
    # print(lista_predict)

    y_pred = clf.predict(lista_predict)
    if y_pred == 0:
        result_neg = 'NEGATIVO'
    else:
        result_neg = 'POSITIVO'

    # print("Resultado: " + result_neg)

    # teste positivo
    lista_pos = [[-1.28842806816101,-0.906829118728638,-0.503570020198822,0.567652404308319,19,
                  0.69428688287735,-0.835507690906525,-0.182790279388428,0.578023791313171,-0.295725524425507,
                  -0.735871851444244,0.541563928127289,0.38068476319313,0.420203506946564,-0.135454878211021]]

    lista_user = lista_pos
    lista_predict = pd.DataFrame(lista_user)
    lista_predict.columns = list(x.columns)
    # print(lista_predict)

    y_pred = clf.predict(lista_predict)
    if y_pred == 0:
        result_pos = 'NEGATIVO'
    else:
        result_pos = 'POSITIVO'

    # print("Resultado: " + result_pos)


    params = clf.get_params()

    response = {
        'acuracia' : acc,
        'result' : result,
        'param_mlpc' : params,
        'result_pos': result_pos,
        'result_neg': result_neg
    }

    return response


class FloatConverter:
    regex = '[\-?\d\.\d\d]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return '{}'.format(value)


def triple_graph(confirmed_data, dead_data, recovered_data, country='Brazil'):
    df_conf = confirmed_data.loc[confirmed_data['country'] == country]
    df_dead = dead_data.loc[dead_data['country'] == country]
    df_recov = recovered_data.loc[recovered_data['country'] == country]

    df_conf.rename(columns={'count': 'count_conf'}, inplace=True)
    df_dead.rename(columns={'count': 'count_dead'}, inplace=True)
    df_recov.rename(columns={'count': 'count_recov'}, inplace=True)

    triple_data = pd.concat([df_conf, df_dead, df_recov],
                            axis=1)
    triple_data = triple_data.loc[triple_data['count_conf'] > 50]
    triple_data.reset_index(inplace=True)

    return triple_data


def plot_triple_graph(triple_graph_data, country_list=('Brazil',)):

    fig = go.Figure()

    for l in country_list:
        fig.add_trace(
            go.Scatter(
                name=str(l) + " Dead",
                y=triple_graph_data['count_dead'],
                x=triple_graph_data.index,
                fill='tonexty',
                line=dict(color='rgb(239,84, 59)'),
            )
        )
        fig.add_trace(
            go.Scatter(
                name=str(l) + " Confirmed",
                y=triple_graph_data['count_conf'],
                x=triple_graph_data.index,
                fill='tonexty',
                line=dict(color='rgb(98, 109, 251)'),
            )
        )
        fig.add_trace(
            go.Scatter(
                name=str(l) + " Recovered",
                y=triple_graph_data['count_recov'],
                x=triple_graph_data.index,
                fill='tozeroy',
                line=dict(color='rgb(0, 204, 150)'),
            )
        )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title='Curva progressão casos - Brasil'
    )

    fig.update_xaxes(title_text='# Dias desde a confirmação de 50 casos', showline=True,
                     linewidth=1,
                     linecolor='rgb(128,128,128)', showgrid=True, gridwidth=0.5,
                     gridcolor='rgb(240,240,240)')
    fig.update_yaxes(title_text='# de casos', showline=True, linewidth=1,
                     linecolor='rgb(128,128,128)', showgrid=True, gridwidth=0.5,
                     gridcolor='rgb(240,240,240)')

    chart = py.plot(
        fig,
        show_link=False,
        output_type='div',
        include_plotlyjs=False,
        auto_open=False,
    )

    return chart
