# Generated by Django 2.2.15 on 2020-08-26 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("powerwiki", "0002_wiki_markup_engine"),
    ]

    operations = [
        migrations.RenameField(model_name="asset", old_name="image", new_name="file",),
    ]
