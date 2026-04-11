from django.shortcuts import render, redirect, get_object_or_404

from partidos.models import Equipo, Partido, TablaGrupo, Grupo
from django.db.models import Q
from itertools import combinations
# Create your views here.

def base(request):
    return render(request, 'base.html')

def grupo(request, letra):

    # obtener grupo
    grupo = Grupo.objects.get(nombre=letra)

    equipos = Equipo.objects.filter(grupo=grupo)
    encuentros =  list(combinations(equipos, 2))

    # calcular tabla
    calcular_tabla(grupo)

    partidos = []

    # obtener tabla ordenada
    tabla = TablaGrupo.objects.filter(grupo=grupo).order_by("-puntos")

    for e in encuentros:
        partidos.append({
            "jornada": 1,
            "local": e[0].nombre,
            "visitante": e[1].nombre,
            "goles_local": 0,
            "goles_visitante": 0
        })


    # MVP dummy
    mvp = [
        {
            "nombre": "Christian Pulisic",
            "equipo": "USA",
            "foto": "https://cdn-icons-png.flaticon.com/512/149/149071.png"
        },
        {
            "nombre": "Santiago Gimenez",
            "equipo": "Mexico",
            "foto": "https://cdn-icons-png.flaticon.com/512/149/149071.png"
        }
    ]

    return render(request, "grupo.html", {
        "grupo": letra,
        "tabla": tabla,
        "partidos": partidos,
        "mvp": mvp,
    })

def playoffs(request):
    calcular_tabla_global()

    tabla_global = TablaGrupo.objects.select_related("equipo", "grupo").order_by(
        "-puntos",
        "-goles_favor",
        "goles_contra"
    )
    top32 = list(tabla_global[:32])

    seed_pairs_32 = [
        (0, 31),
        (15, 16),
        (7, 24),
        (8, 23),
        (3, 28),
        (12, 19),
        (4, 27),
        (11, 20),
        (1, 30),
        (14, 17),
        (6, 25),
        (9, 22),
        (2, 29),
        (13, 18),
        (5, 26),
        (10, 21),
    ]

    def build_match(team_a, team_b, fase):
        return {
            "fase": fase,
            "equipo1": team_a,
            "equipo2": team_b,
            "goles1": 0,
            "goles2": 0,
            "score": "TBD",
        }

    def winner(match):
        if not match["equipo1"] or not match["equipo2"]:
            return None
        if match["goles1"] > match["goles2"]:
            return match["equipo1"]
        if match["goles2"] > match["goles1"]:
            return match["equipo2"]
        return None

    def loser(match):
        if not match["equipo1"] or not match["equipo2"]:
            return None
        if match["goles1"] > match["goles2"]:
            return match["equipo2"]
        if match["goles2"] > match["goles1"]:
            return match["equipo1"]
        return None

    eliminatoria = []
    for a, b in seed_pairs_32:
        team_a = top32[a].equipo if a < len(top32) else None
        team_b = top32[b].equipo if b < len(top32) else None
        eliminatoria.append(build_match(team_a, team_b, "Eliminatoria de 32"))

    octavos = []
    if len(eliminatoria) >= 2:
        octavos = [
            build_match(winner(eliminatoria[0]), winner(eliminatoria[1]), "Octavos"),
            build_match(winner(eliminatoria[2]), winner(eliminatoria[3]), "Octavos"),
            build_match(winner(eliminatoria[4]), winner(eliminatoria[5]), "Octavos"),
            build_match(winner(eliminatoria[6]), winner(eliminatoria[7]), "Octavos"),
            build_match(winner(eliminatoria[8]), winner(eliminatoria[9]), "Octavos"),
            build_match(winner(eliminatoria[10]), winner(eliminatoria[11]), "Octavos"),
            build_match(winner(eliminatoria[12]), winner(eliminatoria[13]), "Octavos"),
            build_match(winner(eliminatoria[14]), winner(eliminatoria[15]), "Octavos"),
        ]

    cuartos = []
    if len(octavos) >= 2:
        cuartos = [
            build_match(winner(octavos[0]), winner(octavos[1]), "Cuartos"),
            build_match(winner(octavos[2]), winner(octavos[3]), "Cuartos"),
            build_match(winner(octavos[4]), winner(octavos[5]), "Cuartos"),
            build_match(winner(octavos[6]), winner(octavos[7]), "Cuartos"),
        ]

    semifinales = []
    if len(cuartos) >= 2:
        semifinales = [
            build_match(winner(cuartos[0]), winner(cuartos[1]), "Semifinal"),
            build_match(winner(cuartos[2]), winner(cuartos[3]), "Semifinal"),
        ]

    final = []
    tercer_puesto = []
    if len(semifinales) >= 2:
        final = [build_match(winner(semifinales[0]), winner(semifinales[1]), "Final")]
        tercer_puesto = [
            build_match(loser(semifinales[0]), loser(semifinales[1]), "Tercer Puesto")
        ]

    return render(request, "playoffs.html", {
        "top32": top32,
        "eliminatoria": eliminatoria,
        "octavos": octavos,
        "cuartos": cuartos,
        "semifinales": semifinales,
        "final": final,
        "tercer_puesto": tercer_puesto,
    })

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

def calcular_tabla_global():
    for grupo in Grupo.objects.all():
        calcular_tabla(grupo)

def editar_equipo(request, id):

    equipo = get_object_or_404(Equipo, id=id)
    grupos = Grupo.objects.all()

    if request.method == "POST":

        equipo.nombre = request.POST.get("nombre")
        equipo.bandera = request.POST.get("bandera")
        equipo.grupo_id = request.POST.get("grupo")

        equipo.save()

        return redirect("/equipos")

    return render(request, "editar_equipo.html", {
        "equipo": equipo,
        "grupos": grupos
    })