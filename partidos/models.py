from django.db import models

# Create your models here.

class Grupo(models.Model):
    nombre = models.CharField(max_length=50)    

class Equipo(models.Model):
    nombre = models.CharField(max_length=50)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)    
    bandera = models.CharField(max_length=200)     


class Partido (models.Model):
    equipo1 = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo1')
    equipo2 = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo2')
    goles_equipo1 = models.IntegerField()
    goles_equipo2 = models.IntegerField()
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

class TablaGrupo(models.Model):

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    jugados = models.IntegerField(default=0)
    ganados = models.IntegerField(default=0)
    empatados = models.IntegerField(default=0)
    perdidos = models.IntegerField(default=0)

    goles_favor = models.IntegerField(default=0)
    goles_contra = models.IntegerField(default=0)

    puntos = models.IntegerField(default=0)
        

class Playoff(models.Model):

    fase = models.CharField(max_length=50)

    equipo1 = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="playoff1"
    )

    equipo2 = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="playoff2"
    )

    goles1 = models.IntegerField(default=0)
    goles2 = models.IntegerField(default=0)