from django.db import migrations, models


def backfill_coordinador_equipo(apps, schema_editor):
    Usuario = apps.get_model('academico', 'Usuario')
    CoordinadorEquipo = apps.get_model('academico', 'CoordinadorEquipo')

    usuarios = Usuario.objects.select_related('id_rol').exclude(id_equipo__isnull=True)
    for usuario in usuarios:
        rol_nombre = (getattr(usuario.id_rol, 'nombre', '') or '').lower()
        es_coordinador = 'coordinador' in rol_nombre
        es_dinamizador_coord = 'dinamizador' in rol_nombre and (usuario.tipo_dinamizador or '') == 'coordinador'
        if es_coordinador or es_dinamizador_coord:
            CoordinadorEquipo.objects.get_or_create(
                id_coordinador_id=usuario.id_usuario,
                id_equipo_id=usuario.id_equipo_id,
            )


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0007_usuario_sin_acceso'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoordinadorEquipo',
            fields=[
                ('id_coordinador_equipo', models.AutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('id_coordinador', models.ForeignKey(db_column='id_coordinador', on_delete=models.deletion.DO_NOTHING, related_name='coordinador_equipos', to='academico.usuario')),
                ('id_equipo', models.ForeignKey(db_column='id_equipo', on_delete=models.deletion.DO_NOTHING, related_name='equipos_por_coordinador', to='academico.equipoejecutor')),
            ],
            options={
                'db_table': 'coordinador_equipo',
                'unique_together': {('id_coordinador', 'id_equipo')},
            },
        ),
        migrations.RunPython(backfill_coordinador_equipo, migrations.RunPython.noop),
    ]
