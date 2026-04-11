from django.core.management.base import BaseCommand
from partidos.models import Grupo
import string


class Command(BaseCommand):

    help = "Crear grupos del mundial (A-L)"

    def handle(self, *args, **kwargs):

        letras = list(string.ascii_uppercase[:12])  # A-L

        for letra in letras:

            grupo, creado = Grupo.objects.get_or_create(nombre=letra)

            if creado:
                self.stdout.write(self.style.SUCCESS(f"Grupo {letra} creado"))
            else:
                self.stdout.write(f"Grupo {letra} ya existe")

        self.stdout.write(self.style.SUCCESS("Grupos listos ⚽"))