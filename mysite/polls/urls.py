from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("index/", views.index),
    path("set/", views.set),
    path("about/", views.about),
    path("access/<int:age>", views.access),
    path('register/', views.register, kwargs={"name":"Паша", "age":"12"}, name='register'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

]