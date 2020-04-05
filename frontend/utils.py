import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

import pandas as pd
import numpy as np


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
                #print(i,j,qtde_dias)
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