from django.urls import path
from . import views

urlpatterns = [
    path('', views.triviabyte_view, name='index'),
    path('get-question/', views.get_questions, name='get_questions'),
    # path('api/get_questions/', views.get_questions, name="get_questions"),
    path('questions/', views.questions, name="questions"),
    path('api/calculate_questions_score/', views.calculate_questions_score, name='calculate_questions_score')
]