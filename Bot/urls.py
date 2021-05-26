from django.urls import path
from Bot import views
# from Bot.views import bot

urlpatterns = [
    path('', views.bot, name='home')
]
