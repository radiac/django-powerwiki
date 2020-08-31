# Generated by Django 2.2.15 on 2020-08-17 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("powerwiki", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="wiki",
            name="markup_engine",
            field=models.CharField(
                choices=[
                    ("powerwiki.markup.rest.RestructuredText", "RestructuredText"),
                    ("powerwiki.markup.md.Markdown", "Markdown"),
                ],
                default="powerwiki.markup.rest.RestructuredText",
                max_length=255,
            ),
        ),
    ]