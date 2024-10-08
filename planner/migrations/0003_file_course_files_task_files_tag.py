# Generated by Django 5.1 on 2024-08-19 21:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_studysession_reminder_task_reminder'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('name', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planner.course')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planner.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='files',
            field=models.ManyToManyField(blank=True, related_name='courses', to='planner.file'),
        ),
        migrations.AddField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='planner.file'),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
