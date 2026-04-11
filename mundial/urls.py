
from django.contrib import admin
from django.urls import path
from partidos.views import base, grupo, playoffs,editar_equipo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', base),
    path('playoffs/', playoffs, name='playoffs'),
    path('grupo/<str:letra>/', grupo, name='grupo'),
    path("equipo/editar/<int:id>/", editar_equipo)
]
