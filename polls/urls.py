from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('new/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('', views.IndexView.as_view(), name='index'),
]
