# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uzewiki.models
from django.conf import settings
import uzewiki.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(help_text=b'Internal name for the asset')),
                ('image', models.ImageField(upload_to=uzewiki.models.asset_upload_to)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', uzewiki.fields.WikiSlugField(help_text=b'Slug for the page', max_length=100)),
                ('title', models.CharField(help_text=b'Title of the page', max_length=255)),
                ('is_locked', models.BooleanField(default=False, help_text=b'If locked, can only be edited by wiki admin')),
                ('content', models.TextField(help_text=b'Page content', blank=True)),
            ],
            options={
                'ordering': ('title',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wiki',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Title of the wiki', max_length=255)),
                ('slug', models.SlugField(help_text=b'Slug for the wiki', unique=True)),
                ('description', models.TextField(help_text=b'Description of wiki', blank=True)),
                ('perm_read', models.IntegerField(default=3, help_text=b'Default read permissions', verbose_name=b'Read permission', choices=[(3, b'Superusers only'), (2, b'Staff only'), (1, b'All users'), (0, b'Public')])),
                ('perm_edit', models.IntegerField(default=3, help_text=b'Default edit permissions', verbose_name=b'Edit permission', choices=[(3, b'Superusers only'), (2, b'Staff only'), (1, b'All users'), (0, b'Public')])),
            ],
            options={
                'ordering': ('title',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WikiPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('can_read', models.BooleanField(default=True, help_text=b'User can read the wiki')),
                ('can_edit', models.BooleanField(default=True, help_text=b'User can edit the wiki')),
                ('user', models.ForeignKey(related_name='wiki_permissions', to=settings.AUTH_USER_MODEL)),
                ('wiki', models.ForeignKey(related_name='user_permissions', to='uzewiki.Wiki')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='wiki',
            name='users',
            field=models.ManyToManyField(related_name='wikis', through='uzewiki.WikiPermissions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='wiki',
            field=models.ForeignKey(related_name='pages', to='uzewiki.Wiki'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('wiki', 'slug')]),
        ),
        migrations.AddField(
            model_name='asset',
            name='wiki',
            field=models.ForeignKey(related_name='assets', to='uzewiki.Wiki'),
            preserve_default=True,
        ),
    ]
