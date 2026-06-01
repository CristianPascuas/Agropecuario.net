from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0002_rename_equipo_activo_to_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='radicado',
            name='empresa_organizacion',
            field=models.CharField(blank=True, default='', max_length=180),
        ),
        migrations.AddField(
            model_name='radicado',
            name='nit',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AddField(
            model_name='radicado',
            name='lugar',
            field=models.CharField(blank=True, default='', max_length=180),
        ),
    ]
