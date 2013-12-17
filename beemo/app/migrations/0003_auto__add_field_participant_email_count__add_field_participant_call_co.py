# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Participant.email_count'
        db.add_column(u'app_participant', 'email_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Participant.call_count'
        db.add_column(u'app_participant', 'call_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Participant.sms_count'
        db.add_column(u'app_participant', 'sms_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Participant.email_count'
        db.delete_column(u'app_participant', 'email_count')

        # Deleting field 'Participant.call_count'
        db.delete_column(u'app_participant', 'call_count')

        # Deleting field 'Participant.sms_count'
        db.delete_column(u'app_participant', 'sms_count')


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
            'call_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'email_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'phone_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Phone']", 'symmetrical': 'False'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '60', 'primary_key': 'True'}),
            'sms_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
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