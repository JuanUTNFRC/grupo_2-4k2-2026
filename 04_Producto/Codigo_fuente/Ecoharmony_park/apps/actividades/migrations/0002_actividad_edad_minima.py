from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='edad_minima',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
