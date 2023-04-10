# Generated by Django 4.1.5 on 2023-04-09 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepageapp', '0004_customerphonesnewsql02model'),
    ]

    operations = [
        migrations.CreateModel(
            name='MakesNewSQL02Model',
            fields=[
                ('make_id', models.AutoField(primary_key=True, serialize=False)),
                ('make_name', models.CharField(max_length=30, null=True)),
                ('make_created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'make',
                'verbose_name_plural': 'makes',
                'db_table': 'makes_new_03',
                'ordering': ['-make_id'],
            },
        ),
        migrations.CreateModel(
            name='ModelsNewSQL02Model',
            fields=[
                ('model_id', models.AutoField(primary_key=True, serialize=False)),
                ('model_name', models.CharField(max_length=30, null=True)),
                ('model_created_at', models.DateTimeField(auto_now_add=True)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepageapp.makesnewsql02model')),
            ],
            options={
                'verbose_name': 'model',
                'verbose_name_plural': 'models',
                'db_table': 'models_new_03',
                'ordering': ['-model_id', 'make'],
            },
        ),
    ]
