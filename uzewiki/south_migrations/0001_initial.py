# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Wiki'
        db.create_table(u'uzewiki_wiki', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('can_read', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('can_edit', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'uzewiki', ['Wiki'])

        # Adding model 'WikiPermissions'
        db.create_table(u'uzewiki_wikipermissions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiki_permissions', to=orm['auth.User'])),
            ('wiki', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_permissions', to=orm['uzewiki.Wiki'])),
            ('can_read', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('can_edit', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'uzewiki', ['WikiPermissions'])

        # Adding model 'Page'
        db.create_table(u'uzewiki_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wiki', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages', to=orm['uzewiki.Wiki'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('is_locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('_content_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'uzewiki', ['Page'])

        # Adding model 'Asset'
        db.create_table(u'uzewiki_asset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wiki', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assets', to=orm['uzewiki.Wiki'])),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'uzewiki', ['Asset'])


    def backwards(self, orm):
        # Deleting model 'Wiki'
        db.delete_table(u'uzewiki_wiki')

        # Deleting model 'WikiPermissions'
        db.delete_table(u'uzewiki_wikipermissions')

        # Deleting model 'Page'
        db.delete_table(u'uzewiki_page')

        # Deleting model 'Asset'
        db.delete_table(u'uzewiki_asset')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'uzewiki.asset': {
            'Meta': {'object_name': 'Asset'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'wiki': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assets'", 'to': u"orm['uzewiki.Wiki']"})
        },
        u'uzewiki.page': {
            'Meta': {'object_name': 'Page'},
            '_content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'wiki': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': u"orm['uzewiki.Wiki']"})
        },
        u'uzewiki.wiki': {
            'Meta': {'object_name': 'Wiki'},
            'can_edit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'can_read': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'through': u"orm['uzewiki.WikiPermissions']", 'to': u"orm['auth.User']"})
        },
        u'uzewiki.wikipermissions': {
            'Meta': {'object_name': 'WikiPermissions'},
            'can_edit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'can_read': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiki_permissions'", 'to': u"orm['auth.User']"}),
            'wiki': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_permissions'", 'to': u"orm['uzewiki.Wiki']"})
        }
    }

    complete_apps = ['uzewiki']