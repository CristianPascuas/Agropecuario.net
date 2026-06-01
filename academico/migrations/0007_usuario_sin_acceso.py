from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0006_populate_tipo_dinamizador'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='sin_acceso',
            field=models.BooleanField(default=False),
        ),
    ]
