# Generated by Django 5.1.3 on 2025-01-10 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
        ('testerapp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.AlterField(
            model_name='test',
            name='groups',
            field=models.ManyToManyField(related_name='tests', to='application.group'),
        ),
    ]
