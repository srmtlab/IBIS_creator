# Generated by Django 2.1.7 on 2019-03-01 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_name', models.TextField()),
                ('node_type', models.CharField(max_length=10)),
                ('node_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NodeNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='IBIS_creator.Node')),
                ('parent_node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='IBIS_creator.Node')),
            ],
        ),
        migrations.CreateModel(
            name='RelevantInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relevant_url', models.URLField()),
                ('relevant_title', models.TextField()),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relevant_info', to='IBIS_creator.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_name', models.TextField()),
                ('theme_description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='node',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='IBIS_creator.Theme'),
        ),
    ]
