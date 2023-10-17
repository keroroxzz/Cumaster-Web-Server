from django.urls import path

import gamecore.views as views

urlpatterns = [
    path('step', views.step, name='step'),
    path('update', views.update, name='update'),
    path('pick', views.pick, name='pick'),
]
