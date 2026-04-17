
from django.contrib import admin
from django.urls import path
from partidos.views import base, grupo, playoffs, editar_equipo, actualizar_resultado, actualizar_resultado_playoff, eliminar_playoff, randomizar_resultado_playoff

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', base),
    path('playoffs/', playoffs, name='playoffs'),
    path('grupo/<str:letra>/', grupo, name='grupo'),
    path("equipo/editar/<int:id>/", editar_equipo, name='editar_equipo'),
    path("partido/actualizar-resultado/", actualizar_resultado, name='actualizar_resultado'),
    path("playoff/actualizar-resultado/", actualizar_resultado_playoff, name='actualizar_resultado_playoff'),
    path("playoff/eliminar/", eliminar_playoff, name='eliminar_playoff'),
    path("playoff/random-resultado/", randomizar_resultado_playoff, name='randomizar_resultado_playoff'),
]
