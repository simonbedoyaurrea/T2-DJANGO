from django.core.management.base import BaseCommand
from partidos.models import Grupo, Equipo


class Command(BaseCommand):

    help = "Crear equipos del mundial"

    def handle(self, *args, **kwargs):

        equipos_por_grupo = {

            "A": [
                ("Mexico", "MX"),
                ("Sudafrica", "ZA"),
                ("Corea del Sur", "KR"),
                ("Chequia", "CZ"),
            ],

            "B": [
                ("Canada", "CA"),
                ("Bosnia", "BA"),
                ("Catar", "QA"),
                ("Suiza", "CH"),
            ],

            "C": [
                ("Brasil", "BR"),
                ("Marruecos", "MA"),
                ("Haiti", "HT"),
                ("Escocia", "GB-SCT"),
            ],

            "D": [
                ("Estados Unidos", "US"),
                ("Paraguay", "PY"),
                ("Australia", "AU"),
                ("Turquia", "TR"),
            ],

            "E": [
                ("Alemania", "DE"),
                ("Curazao", "CW"),
                ("Costa de Marfil", "CI"),
                ("Ecuador", "EC"),
            ],

            "F": [
                ("Paises Bajos", "NL"),
                ("Japon", "JP"),
                ("Suecia", "SE"),
                ("Tunez", "TN"),
            ],

            "G": [
                ("Belgica", "BE"),
                ("Egipto", "EG"),
                ("Iran", "IR"),
                ("Nueva Zelanda", "NZ"),
            ],

            "H": [
                ("España", "ES"),
                ("Cabo Verde", "CV"),
                ("Arabia Saudita", "SA"),
                ("Uruguay", "UY"),
            ],

            "I": [
                ("Francia", "FR"),
                ("Senegal", "SN"),
                ("Irak", "IQ"),
                ("Noruega", "NO"),
            ],

            "J": [
                ("Argentina", "AR"),
                ("Argelia", "DZ"),
                ("Austria", "AT"),
                ("Jordania", "JO"),
            ],

            "K": [
                ("Portugal", "PT"),
                ("RD Congo", "CD"),
                ("Uzbekistan", "UZ"),
                ("Colombia", "CO"),
            ],

            "L": [
                ("Inglaterra", "GB-ENG"),
                ("Croacia", "HR"),
                ("Ghana", "GH"),
                ("Panama", "PA"),
            ],

        }

        for letra, equipos in equipos_por_grupo.items():

            grupo = Grupo.objects.get(nombre=letra)

            for nombre, codigo_bandera in equipos:

                bandera_url = f"https://flagsapi.com/{codigo_bandera}/flat/64.png"

                Equipo.objects.get_or_create(
                    nombre=nombre,
                    grupo=grupo,
                    bandera=bandera_url
                )

                self.stdout.write(f"{nombre} agregado al grupo {letra}")

        self.stdout.write(self.style.SUCCESS("Equipos creados correctamente ⚽"))