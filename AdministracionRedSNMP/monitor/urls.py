from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from monitor import views
#from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'images', views.ImageViewSet)


urlpatterns = [
    #path('', include(router.urls)),
    path('Agentes', views.verAgentes, name='agentes'),
    path('Agregar', views.agregarAgente, name='agregar'),
    path('Proyeccion',views.verProyeccion, name='proyeccion'),
    path('Inventario',views.verRouters, name='inventario'),
    path('FormularioSubirArchivo',views.cargarArchivosConf, name='subir'),
    #path('BajarArchivo',views.bajarArchivosConf, name='bajar'),
    #path('verRouterDetalles',views.obtenerInfoRouter, name='verRouter'),
    path('verRouterDetalles/<name>/',views.obtenerInfoRouter, name='verRouter'),
    #path('Ajax/Proyeccion',views.getImage, name='Ajax/Proyeccion'),
    path('Ver', views.obtenerInfo, name='ver'),
    #path('Actualiza', views.actualizaImg, name='Actualiza'),
    path('Ver/<name>/', views.obtenerInfo, name='ver'),
    path('<int:pk>/detalles/', views.estadoAgente, name='detalle'),
    path('Borrar/<name>', views.deleteAgent, name='borrar'),
    path('SubirArchivo', views.subirArchivoConf, name='upload'),
    path('BajarArchivo', views.bajarArchivoConf, name='download')
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    
]

urlpatterns += staticfiles_urlpatterns()
