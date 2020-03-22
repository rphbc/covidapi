import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff




def plotlinechart(data_list, plot_name):
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=[10, 20, None, 15, 10, 5, 15, None, 20, 10, 10, 15, 25, 20, 10],
        name='<b>No</b> Gaps',  # Style name/legend entry with html tags
        connectgaps=True  # override default to connect the gaps
    ))

    chart = py.plot(
        fig,
        show_link=False,
        output_type='div',
        include_plotlyjs=False,
        auto_open=False,
    )

    return chart