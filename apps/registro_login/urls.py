from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registro', views.registro),
    path('login', views.login),
    path('wall/<int:id_user>', views.wall),
    path('logout', views.logout),
    path('agregar_libro', views.agregar_libro),
    path('detalle_libro/<int:id_book>', views.detalle_libro),
    path('eliminar_review/<int:id_review>',views.eliminar_review),
    path('perfil_usuario/<int:id_user>',views.perfil_usuario),
    
]