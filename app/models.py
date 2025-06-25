from django.db import models
from django.conf import settings


class Favourite(models.Model):
    # Detalles del pokemon.
    pokemon_id = models.IntegerField() #ID de pokeapi
    name = models.CharField(max_length=200)  # Nombre del personaje
    height = models.CharField(max_length=200)  # Altura
    weight = models.CharField(max_length=200)  # Peso
    base_experience = models.IntegerField(null=True, blank=True)  # Experiencia base
    types = models.JSONField(default=list)  # Lista de tipos (ej: ["grass", "poison"])
    image = models.URLField()  # URL de la imagen

    # Asociamos el favorito con el usuario que lo guarda.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        # Restringe duplicados: un mismo usuario no puede guardar el mismo personaje varias veces.
        unique_together = (('user', 'pokemon_id'),)

    def __str__(self):
        return f"{self.name} (ID: {self.pokemon_id}) - {self.user.username}"
