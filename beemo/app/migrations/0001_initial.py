# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Participant'
        db.create_table(u'app_participant', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=60, primary_key=True)),
            ('coach', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Participant'])


    def backwards(self, orm):
        # Deleting model 'Participant'
        db.delete_table(u'app_participant')


    models = {
        u'app.participant': {
            'Meta': {'object_name': 'Participant'},
            'coach': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '60', 'primary_key': 'True'})
        }
    }

    complete_apps = ['app']