# Generated by Django 4.1.5 on 2023-04-09 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepageapp', '0002_rename_vechicle_used_level_vehiclesnewsql02model_vehicle_used_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerEmailsNewSQL02Model',
            fields=[
                ('customeremail_id', models.AutoField(primary_key=True, serialize=False)),
                ('customeremail_is_selected', models.BooleanField(default=True)),
                ('customeremail_created_at', models.DateTimeField(auto_now_add=True)),
                ('customeremail_last_updated_date', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepageapp.customersnewsql02model')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepageapp.emailsnewsql02model')),
            ],
            options={
                'db_table': 'customeremails_new_03',
                'ordering': ['-customeremail_id', '-email'],
            },
        ),
    ]
