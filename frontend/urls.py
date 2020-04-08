from django.urls import path,register_converter
from frontend.views import Home, Simulation, Diagnose, predict, result_predict, vote, result_vote
from frontend.utils import FloatConverter

register_converter(FloatConverter, 'float')
app_name = 'frontend'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('simulation', Simulation.as_view(), name='simulation'),
    path('diagnose', Diagnose.as_view(), name='diagnose'),
    path('vote', vote, name='vote'),
    path('<int:question_id>/<int:question_id2>/vote', result_vote, name='result_vote'),
    path('predict', predict, name='predict'),
    path('<float:question_id1>/<float:question_id2>/<float:question_id3>/<float:question_id4>/<float:question_id5>/'
         '<float:question_id6>/<float:question_id7>/<float:question_id8>/<float:question_id9>/<float:question_id10>/'
         '<float:question_id11>/<float:question_id12>/<float:question_id13>/<float:question_id14>/'
         '<float:question_id15>/predict', result_predict, name='result_predict'),
]
