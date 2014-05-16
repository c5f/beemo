# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Call.adherence_score'
        db.add_column(u'app_call', 'adherence_score',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)


        # Changing field 'Call.fiber_grams'
        db.alter_column(u'app_call', 'fiber_grams', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'Call.veg_servings'
        db.alter_column(u'app_call', 'veg_servings', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'Call.fat_grams'
        db.alter_column(u'app_call', 'fat_grams', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'Call.steps'
        db.alter_column(u'app_call', 'steps', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'Call.fruit_servings'
        db.alter_column(u'app_call', 'fruit_servings', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Call.adherence_score'
        db.delete_column(u'app_call', 'adherence_score')


        # Changing field 'Call.fiber_grams'
        db.alter_column(u'app_call', 'fiber_grams', self.gf('django.db.models.fields.PositiveIntegerField')(default=None))

        # Changing field 'Call.veg_servings'
        db.alter_column(u'app_call', 'veg_servings', self.gf('django.db.models.fields.PositiveIntegerField')(default=None))

        # Changing field 'Call.fat_grams'
        db.alter_column(u'app_call', 'fat_grams', self.gf('django.db.models.fields.PositiveIntegerField')(default=None))

        # Changing field 'Call.steps'
        db.alter_column(u'app_call', 'steps', self.gf('django.db.models.fields.PositiveIntegerField')(default=None))

        # Changing field 'Call.fruit_servings'
        db.alter_column(u'app_call', 'fruit_servings', self.gf('django.db.models.fields.PositiveIntegerField')(default=None))

    models = {
        'app.call': {
            'Meta': {'object_name': 'Call'},
            'adherence_score': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'completed_date': ('django.db.models.fields.DateField', [], {}),
            'fat_grams': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'fiber_grams': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'fruit_servings': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'goal_met': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calls'", 'to': "orm['app.Participant']"}),
            'steps': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'veg_servings': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'app.email': {
            'Meta': {'object_name': 'Email'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'to': "orm['app.Participant']"})
        },
        'app.participant': {
            'Meta': {'object_name': 'Participant'},
            'base_fat_goal': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'base_step_goal': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'phone_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Phone']", 'symmetrical': 'False'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '60', 'primary_key': 'True'}),
            'sms_number': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sms_participant'", 'null': 'True', 'to': "orm['app.Phone']"})
        },
        'app.participantproblem': {
            'Meta': {'object_name': 'ParticipantProblem'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Participant']"}),
            'problem': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'app.phone': {
            'Meta': {'object_name': 'Phone'},
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'})
        }
    }

    complete_apps = ['app']