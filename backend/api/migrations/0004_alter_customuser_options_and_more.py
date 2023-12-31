# Generated by Django 4.0.10 on 2023-09-19 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_customuser_jobs_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together={('username', 'email')},
        ),
        migrations.AlterIndexTogether(
            name='customuser',
            index_together={('username', 'email')},
        ),
    ]
