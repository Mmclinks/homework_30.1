# Generated by Django 5.1.4 on 2024-12-10 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="course",
            options={},
        ),
        migrations.AlterModelOptions(
            name="lesson",
            options={},
        ),
        migrations.RemoveField(
            model_name="course",
            name="photo",
        ),
        migrations.RemoveField(
            model_name="course",
            name="title",
        ),
        migrations.RemoveField(
            model_name="lesson",
            name="photo",
        ),
        migrations.RemoveField(
            model_name="lesson",
            name="title",
        ),
        migrations.AddField(
            model_name="course",
            name="name",
            field=models.CharField(
                default="Курс", max_length=255, verbose_name="Название курса"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="preview",
            field=models.ImageField(
                default="courses/previews/course.png", upload_to="courses/previews/"
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="name",
            field=models.CharField(
                default="Урок", max_length=255, verbose_name="Название урока"
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="preview",
            field=models.ImageField(
                default="lessons/previews/lesson.png", upload_to="lessons/previews/"
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="description",
            field=models.TextField(verbose_name="Описание курса"),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="description",
            field=models.TextField(verbose_name="Описание урока/"),
        ),
    ]
