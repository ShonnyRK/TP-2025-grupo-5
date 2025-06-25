from django.db import migrations

def delete_null_pokemon_id(apps, schema_editor):
    Favourite = apps.get_model('app', 'Favourite')
    Favourite.objects.filter(pokemon_id__isnull=True).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0004_copy_id_to_pokemon_id'),
    ]
    operations = [
        migrations.RunPython(delete_null_pokemon_id),
    ] 