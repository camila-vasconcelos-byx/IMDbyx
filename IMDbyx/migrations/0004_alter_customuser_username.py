# Generated by Django 5.1.4 on 2024-12-20 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IMDbyx', '0003_remove_customuser_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, null=True),
        ),
    ]