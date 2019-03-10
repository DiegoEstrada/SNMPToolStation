from django.urls import path
from monitor import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('Agentes', views.verAgentes, name='agentes'),
    path('Agregar', views.agregarAgente, name='agregar'),
    path('Proyeccion',views.verProyeccion, name='proyeccion'),
    path('Ver', views.obtenerInfo, name='ver'),
    path('Ver/<nombreHost>/', views.obtenerInfo, name='ver'),
    path('<int:pk>/detalles/', views.estadoAgente, name='detalle'),
    
]

urlpatterns += staticfiles_urlpatterns()
