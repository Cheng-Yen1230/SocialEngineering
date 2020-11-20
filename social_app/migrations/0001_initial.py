# Generated by Django 3.1.3 on 2020-11-19 10:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('get_id', models.PositiveIntegerField(db_column='流水號', primary_key=True, serialize=False, unique=True, verbose_name='流水號')),
                ('name', models.CharField(db_column='員工姓名', max_length=50, verbose_name='員工姓名')),
                ('email', models.EmailField(db_column='信箱', max_length=254, verbose_name='信箱')),
                ('times', models.PositiveSmallIntegerField(db_column='訪問次數', default=0, verbose_name='訪問次數')),
            ],
            options={
                'db_table': 'tb_data_management',
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_time', models.DateTimeField(db_column='訪問時間', default=django.utils.timezone.now, verbose_name='訪問時間')),
                ('num', models.ForeignKey(db_column='流水號', on_delete=django.db.models.deletion.CASCADE, related_name='data', to='social_app.email')),
            ],
            options={
                'db_table': 'tb_data_all',
            },
        ),
    ]
