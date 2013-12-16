# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table(u'app_email', (
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emails', to=orm['app.Participant'])),
        ))
        db.send_create_signal('app', ['Email'])

        # Adding model 'Phone'
        db.create_table(u'app_phone', (
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
        ))
        db.send_create_signal('app', ['Phone'])

        # Adding model 'Participant'
        db.create_table(u'app_participant', (
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=60, primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('sms_number', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sms_participant', null=True, to=orm['app.Phone'])),
            ('base_fat_goal', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('base_step_goal', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('app', ['Participant'])

        # Adding M2M table for field phone_numbers on 'Participant'
        m2m_table_name = db.shorten_name(u'app_participant_phone_numbers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm['app.participant'], null=False)),
            ('phone', models.ForeignKey(orm['app.phone'], null=False))
        ))
        db.create_unique(m2m_table_name, ['participant_id', 'phone_id'])

        # Adding model 'Call'
        db.create_table(u'app_call', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Participant'])),
            ('completed_date', self.gf('django.db.models.fields.DateField')()),
            ('goal_met', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('veg_servings', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('fruit_servings', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('fiber_grams', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('fat_grams', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('steps', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('app', ['Call'])

        # Adding model 'ParticipantProblem'
        db.create_table(u'app_participantproblem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Participant'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('problem', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('app', ['ParticipantProblem'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table(u'app_email')

        # Deleting model 'Phone'
        db.delete_table(u'app_phone')

        # Deleting model 'Participant'
        db.delete_table(u'app_participant')

        # Removing M2M table for field phone_numbers on 'Participant'
        db.delete_table(db.shorten_name(u'app_participant_phone_numbers'))

        # Deleting model 'Call'
        db.delete_table(u'app_call')

        # Deleting model 'ParticipantProblem'
        db.delete_table(u'app_participantproblem')


    models = {
        'app.call': {
            'Meta': {'object_name': 'Call'},
            'completed_date': ('django.db.models.fields.DateField', [], {}),
            'fat_grams': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'fiber_grams': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'fruit_servings': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'goal_met': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Participant']"}),
            'steps': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'veg_servings': ('django.db.models.fields.PositiveIntegerField', [], {})
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