# Generated by Django 3.2.14 on 2022-07-11 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaidHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('score', models.PositiveIntegerField(default=0)),
                ('enter_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('level', models.PositiveIntegerField()),
                ('raid_status', models.BooleanField(default=False)),
                ('delete_flag', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raid_histories', to='user.user')),
            ],
            options={
                'db_table': 'raid_history',
            },
        ),
    ]
