from django.urls import path
from lang import views
# from Bot.views import bot

urlpatterns = [
    path('', views.lang, name='lang')
]
