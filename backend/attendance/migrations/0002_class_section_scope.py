from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("attendance", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="student",
            name="class_name",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="student",
            name="section",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="attendancesession",
            name="class_name",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="attendancesession",
            name="section",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
