from django.shortcuts import render, redirect, get_object_or_404
import random

from partidos.models import Equipo, Partido, TablaGrupo, Grupo, Playoff
from django.db.models import Q
from itertools import combinations
# Create your views here.

def base(request):
    return render(request, 'base.html')

def grupo(request, letra):

    # obtener grupo
    grupo = Grupo.objects.get(nombre=letra)

    equipos = Equipo.objects.filter(grupo=grupo)

    partidos = Partido.objects.filter(grupo=grupo)  

    if not partidos.exists():
        generar_partidos(grupo.nombre)
        partidos = Partido.objects.filter(grupo=grupo)

    # calcular tabla
    calcular_tabla(grupo)

        # obtener tabla ordenada
    tabla = TablaGrupo.objects.filter(grupo=grupo).order_by("-puntos")

    

    # MVP dummy
    mvp = [
        {
            "nombre": "Kylian Mbappé",
            "equipo": "Francia",
            "foto": "https://img.uefa.com/imgml/TP/players/1/2026/324x324/250076574.jpg"
        },
        {
            "nombre": "Manuel Neuer",
            "equipo": "Alemania",
            "foto": "https://img.a.transfermarkt.technology/portrait/big/17259-1762943283.jpg?lm=1"
        }
    ]

    return render(request, "grupo.html", {
        "grupo": letra,
        "tabla": tabla,
        "partidos": partidos,
        "mvp": mvp,
        "equipos": equipos
    })
def generar_partidos(letra):

    grupo = Grupo.objects.get(nombre=letra)
    equipos = Equipo.objects.filter(grupo=grupo)

    encuentros = list(combinations(equipos, 2))

    for e in encuentros:
        Partido.objects.create(
            equipo1=e[0],
            equipo2=e[1],
            goles_equipo1=0,
            goles_equipo2=0,
            grupo=grupo
        )


def playoffs(request):
    # Generar playoffs si no existen
    if not Playoff.objects.exists():
        generar_playoffs()
    
    # Obtener todas las rondas
    eliminatoria = Playoff.objects.filter(ronda=1).order_by('orden')
    octavos = Playoff.objects.filter(ronda=2).order_by('orden')
    cuartos = Playoff.objects.filter(ronda=3).order_by('orden')
    semifinales = Playoff.objects.filter(ronda=4).order_by('orden')
    final = Playoff.objects.filter(ronda=5).order_by('orden')
    tercer_puesto = Playoff.objects.filter(ronda=6).order_by('orden')
    
    return render(request, "playoffs.html", {
        "eliminatoria": eliminatoria,
        "octavos": octavos,
        "cuartos": cuartos,
        "semifinales": semifinales,
        "final": final,
        "tercer_puesto": tercer_puesto,
    })

def generar_playoffs():
    from partidos.models import Playoff
    
    
    Playoff.objects.all().delete()
    
  
    tabla_global = TablaGrupo.objects.select_related("equipo", "grupo").order_by(
        "-puntos",
        "-goles_favor",
        "goles_contra"
    )
    top32 = list(tabla_global[:32])
    
    
    seed_pairs_32 = [
        (0, 31), (15, 16), (7, 24), (8, 23), (3, 28), (12, 19),
        (4, 27), (11, 20), (1, 30), (14, 17), (6, 25), (9, 22),
        (2, 29), (13, 18), (5, 26), (10, 21),
    ]
    
    # Crear partidos de eliminatoria de 32
    for i, (a, b) in enumerate(seed_pairs_32):
        team_a = top32[a].equipo if a < len(top32) else None
        team_b = top32[b].equipo if b < len(top32) else None
        
        Playoff.objects.create(
            fase="Eliminatoria de 32",
            equipo1=team_a,
            equipo2=team_b,
            ronda=1,
            orden=i
        )

def generar_siguiente_ronda(ronda_actual):
  
    from partidos.models import Playoff
    
    if ronda_actual == 1: 
        partidos_actuales = Playoff.objects.filter(ronda=1)
        ganadores = []
        
        for partido in partidos_actuales:
            if partido.equipo1 and partido.equipo2:
                if partido.goles1 > partido.goles2:
                    ganadores.append(partido.equipo1)
                elif partido.goles2 > partido.goles1:
                    ganadores.append(partido.equipo2)
        
       
        if len(ganadores) >= 16:
            for i in range(8):
                Playoff.objects.create(
                    fase="Octavos",
                    equipo1=ganadores[i*2] if i*2 < len(ganadores) else None,
                    equipo2=ganadores[i*2+1] if i*2+1 < len(ganadores) else None,
                    ronda=2,
                    orden=i
                )
    
    elif ronda_actual == 2: 
        partidos_actuales = Playoff.objects.filter(ronda=2)
        ganadores = []
        
        for partido in partidos_actuales:
            if partido.equipo1 and partido.equipo2:
                if partido.goles1 > partido.goles2:
                    ganadores.append(partido.equipo1)
                elif partido.goles2 > partido.goles1:
                    ganadores.append(partido.equipo2)
        
       
        if len(ganadores) >= 8:
            for i in range(4):
                Playoff.objects.create(
                    fase="Cuartos",
                    equipo1=ganadores[i*2] if i*2 < len(ganadores) else None,
                    equipo2=ganadores[i*2+1] if i*2+1 < len(ganadores) else None,
                    ronda=3,
                    orden=i
                )
    
    elif ronda_actual == 3: 
        partidos_actuales = Playoff.objects.filter(ronda=3)
        ganadores = []
        perdedores = []
        
        for partido in partidos_actuales:
            if partido.equipo1 and partido.equipo2:
                if partido.goles1 > partido.goles2:
                    ganadores.append(partido.equipo1)
                    perdedores.append(partido.equipo2)
                elif partido.goles2 > partido.goles1:
                    ganadores.append(partido.equipo2)
                    perdedores.append(partido.equipo1)
        
        
        if len(ganadores) >= 4:
            for i in range(2):
                Playoff.objects.create(
                    fase="Semifinal",
                    equipo1=ganadores[i*2] if i*2 < len(ganadores) else None,
                    equipo2=ganadores[i*2+1] if i*2+1 < len(ganadores) else None,
                    ronda=4,
                    orden=i
                )
        
        
        if len(perdedores) >= 2:
            Playoff.objects.create(
                fase="Tercer Puesto",
                equipo1=perdedores[0] if len(perdedores) > 0 else None,
                equipo2=perdedores[1] if len(perdedores) > 1 else None,
                ronda=6,
                orden=0
            )
    
    elif ronda_actual == 4:  
        partidos_actuales = Playoff.objects.filter(ronda=4)
        ganadores = []
        
        for partido in partidos_actuales:
            if partido.equipo1 and partido.equipo2:
                if partido.goles1 > partido.goles2:
                    ganadores.append(partido.equipo1)
                elif partido.goles2 > partido.goles1:
                    ganadores.append(partido.equipo2)
        
  
        if len(ganadores) >= 2:
            Playoff.objects.create(
                fase="Final",
                equipo1=ganadores[0] if len(ganadores) > 0 else None,
                equipo2=ganadores[1] if len(ganadores) > 1 else None,
                ronda=5,
                orden=0
            )

def calcular_tabla(grupo):

    equipos = Equipo.objects.filter(grupo=grupo)

    for equipo in equipos:

        partidos = Partido.objects.filter(
            Q(equipo1=equipo) | Q(equipo2=equipo)
        )

        jugados = ganados = empatados = perdidos = 0
        gf = gc = puntos = 0

        for p in partidos:

            if p.equipo1 == equipo:
                gf += p.goles_equipo1
                gc += p.goles_equipo2

                if p.goles_equipo1 > p.goles_equipo2:
                    puntos += 3
                    ganados += 1
                elif p.goles_equipo1 == p.goles_equipo2:
                    puntos += 1
                    empatados += 1
                else:
                    perdidos += 1

            else:
                gf += p.goles_equipo2
                gc += p.goles_equipo1

                if p.goles_equipo2 > p.goles_equipo1:
                    puntos += 3
                    ganados += 1
                elif p.goles_equipo2 == p.goles_equipo1:
                    puntos += 1
                    empatados += 1
                else:
                    perdidos += 1

            jugados += 1


        TablaGrupo.objects.update_or_create(
            equipo=equipo,
            grupo=grupo,
            defaults={
                "jugados": jugados,
                "ganados": ganados,
                "empatados": empatados,
                "perdidos": perdidos,
                "goles_favor": gf,
                "goles_contra": gc,
                "puntos": puntos,
            }
        )


def actualizar_resultado(request):
    if request.method == "POST":
        partido_id = request.POST.get("partido_id")
        goles_equipo1 = int(request.POST.get("goles_equipo1", 0))
        goles_equipo2 = int(request.POST.get("goles_equipo2", 0))
        
        partido = get_object_or_404(Partido, id=partido_id)
        partido.goles_equipo1 = goles_equipo1
        partido.goles_equipo2 = goles_equipo2
        partido.save()
        
        # Recalcular tabla del grupo
        calcular_tabla(partido.grupo)
        
        return redirect("grupo", letra=partido.grupo.nombre)
    
    return redirect("playoffs")

def actualizar_resultado_playoff(request):
    if request.method == "POST":
        playoff_id = request.POST.get("playoff_id")
        goles1 = int(request.POST.get("goles_equipo1", 0))
        goles2 = int(request.POST.get("goles_equipo2", 0))
        
        playoff = get_object_or_404(Playoff, id=playoff_id)
        playoff.goles1 = goles1
        playoff.goles2 = goles2
        playoff.save()
        
        # Generar siguiente ronda si es necesario
        generar_siguiente_ronda(playoff.ronda)
        
        return redirect("playoffs")
    
    return redirect("playoffs")


def randomizar_resultado_playoff(request):
    if request.method == "POST":
        playoff_id = request.POST.get("playoff_id")
        playoff = get_object_or_404(Playoff, id=playoff_id)

        if playoff.equipo1 and playoff.equipo2:
            goles1 = random.randint(1, 5)
            goles2 = random.randint(1, 5)
            while goles1 == goles2:
                goles2 = random.randint(1, 5)

            playoff.goles1 = goles1
            playoff.goles2 = goles2
            playoff.save()
            generar_siguiente_ronda(playoff.ronda)

        return redirect("playoffs")
    return redirect("playoffs")


def eliminar_playoff(request):
    if request.method == "POST":
        playoff_id = request.POST.get("playoff_id")
        playoff = get_object_or_404(Playoff, id=playoff_id)
        playoff.delete()
        return redirect("playoffs")
    
    return redirect("playoffs")


def editar_equipo(request, id):

    equipo = get_object_or_404(Equipo, id=id)
    grupos = Grupo.objects.all()

    if request.method == "POST":

        equipo.nombre = request.POST.get("nombre")
        equipo.bandera = request.POST.get("bandera")
        equipo.grupo_id = request.POST.get("grupo")

        equipo.save()

        return redirect("grupo", letra=equipo.grupo.nombre)

    return render(request, "editar_equipo.html", {
        "equipo": equipo,
        "grupos": grupos
    })

