# Generated by Django 3.2.7 on 2022-04-18 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('section_id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('section_name', models.CharField(max_length=32, unique=True, verbose_name='类型')),
            ],
            options={
                'db_table': 'table_section',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_title', models.CharField(max_length=32)),
                ('source_desc', models.CharField(max_length=255)),
                ('source_url', models.CharField(max_length=255)),
                ('source_section', models.CharField(max_length=32)),
                ('source_time', models.DateTimeField(auto_now_add=True)),
                ('source_author', models.CharField(max_length=32)),
                ('is_delete', models.SmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'table_source',
            },
        ),
    ]