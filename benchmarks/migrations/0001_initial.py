# Generated by Django 4.0.6 on 2022-07-25 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('result', models.JSONField(blank=True, null=True)),
                ('path', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Case',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('smart_before_test_path', models.FileField(blank=True, null=True, upload_to='', verbose_name='Pre S.M.A.R.T Info ')),
                ('smart_after_test_path', models.FileField(blank=True, null=True, upload_to='', verbose_name='Post S.M.A.R.T Info ')),
                ('upload', models.FileField(blank=True, null=True, upload_to='uploads/')),
            ],
            options={
                'verbose_name': 'Project',
            },
        ),
        migrations.CreateModel(
            name='LogFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('path', models.FileField(blank=True, null=True, upload_to='')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='benchmarks.case')),
            ],
            options={
                'verbose_name': 'LogFile',
            },
        ),
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='benchmarks.project')),
            ],
            options={
                'verbose_name': 'Drive',
            },
        ),
        migrations.AddField(
            model_name='case',
            name='drive',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='benchmarks.drive'),
        ),
    ]
