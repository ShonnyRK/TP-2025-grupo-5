from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0005_delete_null_pokemon_id'),
    ]
    operations = [
        migrations.AlterField(
            model_name='favourite',
            name='pokemon_id',
            field=models.IntegerField(),
        ),
    ] 