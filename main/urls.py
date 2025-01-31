
from django.contrib import admin
from django.urls import path,include
from .views import ReloadView,HomeView,StatsView

urlpatterns = [
    path('', HomeView.as_view()),
    path('reload/', ReloadView.as_view()),
    path('stats/',StatsView.as_view())
]
