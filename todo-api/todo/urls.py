from django.urls import path
from .views import *

urlpatterns = [
    path('', TodoGenericsApiView.as_view()),
    path('<int:pk>', TodoGenenricsDetailedApiView.as_view(),name='todo-detail'),
]