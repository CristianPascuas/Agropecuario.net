from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0001_squashed_0007_remove_radicado_fechas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipoejecutor',
            old_name='activo',
            new_name='tipo',
        ),
        migrations.AlterField(
            model_name='equipoejecutor',
            name='tipo',
            field=models.PositiveSmallIntegerField(
                choices=[(0, 'Trasversal'), (1, 'Tecnica')],
                default=1,
            ),
        ),
    ]
