# Generated by Django 4.2.17 on 2025-01-04 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Uploaded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=100)),
                ('book_description', models.TextField()),
                ('visibility', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=10)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('year_of_published', models.PositiveIntegerField()),
            ],
        ),
    ]
