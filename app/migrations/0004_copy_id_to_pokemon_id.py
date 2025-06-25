# Generated manually to copy data from id to pokemon_id

from django.db import migrations


def copy_id_to_pokemon_id(apps, schema_editor):
    Favourite = apps.get_model('app', 'Favourite')
    for favourite in Favourite.objects.all():
        # Copiar el valor del campo id al campo pokemon_id
        favourite.pokemon_id = favourite.id
        favourite.save()


def reverse_copy_id_to_pokemon_id(apps, schema_editor):
    Favourite = apps.get_model('app', 'Favourite')
    for favourite in Favourite.objects.all():
        # Revertir: copiar pokemon_id de vuelta a id
        favourite.id = favourite.pokemon_id
        favourite.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_favourite_unique_together_favourite_pokemon_id_and_more'),
    ]

    operations = [
        migrations.RunPython(copy_id_to_pokemon_id, reverse_copy_id_to_pokemon_id),
    ] 