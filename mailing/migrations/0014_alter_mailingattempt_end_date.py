# Generated by Django 4.2.2 on 2024-09-06 09:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0013_mailing_end_date_alter_mailing_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingattempt',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время окончания рассылки'),
            preserve_default=False,
        ),
    ]
