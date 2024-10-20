from . import views
from django.urls import path

urlpatterns = [
    path('main',views.main),
    path('Abstract',views.Abstract),
    path('upload',views.upload),
    path('main_two_xml', views.main_two_xml),
    path('present_type', views.present_type),
    path('main_statics', views.main_statics),
    path('ajax/initial_chart/', views.initial_chart, name='initial_chart'),
    path('ajax/add_chart/', views.add_chart, name='add_chart'),
]

