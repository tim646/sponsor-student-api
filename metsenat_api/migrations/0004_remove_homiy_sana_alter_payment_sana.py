# Generated by Django 4.1.1 on 2022-09-22 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metsenat_api', '0003_alter_talaba_ajratilgan_summa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homiy',
            name='sana',
        ),
        migrations.AlterField(
            model_name='payment',
            name='sana',
            field=models.DateField(auto_now=True),
        ),
    ]
