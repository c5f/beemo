# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ParticipantProblem'
        db.delete_table(u'app_participantproblem')

        # Deleting model 'Participant'
        db.delete_table(u'app_participant')

        # Removing M2M table for field phone_numbers on 'Participant'
        db.delete_table(db.shorten_name(u'app_participant_phone_numbers'))

        # Adding model 'InterventionParticipant'
        db.create_table(u'app_interventionparticipant', (
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=60, primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('sms_number', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sms_participant', null=True, to=orm['app.Phone'])),
            ('base_fat_goal', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('base_step_goal', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('emails_in', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('emails_out', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('calls_in', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('calls_out', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('sms_in', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('sms_out', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('app', ['InterventionParticipant'])

        # Adding M2M table for field phone_numbers on 'InterventionParticipant'
        m2m_table_name = db.shorten_name(u'app_interventionparticipant_phone_numbers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('interventionparticipant', models.ForeignKey(orm['app.interventionparticipant'], null=False)),
            ('phone', models.ForeignKey(orm['app.phone'], null=False))
        ))
        db.create_unique(m2m_table_name, ['interventionparticipant_id', 'phone_id'])

        # Adding model 'InterventionParticipantProblem'
        db.create_table(u'app_interventionparticipantproblem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.InterventionParticipant'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('problem', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('app', ['InterventionParticipantProblem'])


        # Changing field 'Email.participant'
        db.alter_column(u'app_email', 'participant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.InterventionParticipant']))

        # Changing field 'Call.participant'
        db.alter_column(u'app_call', 'participant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.InterventionParticipant']))

    def backwards(self, orm):
        # Adding model 'ParticipantProblem'
        db.create_table(u'app_participantproblem', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('problem', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Participant'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('app', ['ParticipantProblem'])

        # Adding model 'Participant'
        db.create_table(u'app_participant', (
            ('calls_in', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('base_step_goal', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('sms_out', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('calls_out', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=60, primary_key=True)),
            ('base_fat_goal', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('emails_out', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('sms_number', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sms_participant', null=True, to=orm['app.Phone'], blank=True)),
            ('emails_in', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('sms_in', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
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

        # Deleting model 'InterventionParticipant'
        db.delete_table(u'app_interventionparticipant')

        # Removing M2M table for field phone_numbers on 'InterventionParticipant'
        db.delete_table(db.shorten_name(u'app_interventionparticipant_phone_numbers'))

        # Deleting model 'InterventionParticipantProblem'
        db.delete_table(u'app_interventionparticipantproblem')


        # Changing field 'Email.participant'
        db.alter_column(u'app_email', 'participant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Participant']))

        # Changing field 'Call.participant'
        db.alter_column(u'app_call', 'participant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Participant']))

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
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calls'", 'to': "orm['app.InterventionParticipant']"}),
            'steps': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'veg_servings': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'app.email': {
            'Meta': {'object_name': 'Email'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'to': "orm['app.InterventionParticipant']"})
        },
        'app.interventionparticipant': {
            'Meta': {'object_name': 'InterventionParticipant'},
            'base_fat_goal': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'base_step_goal': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'calls_in': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'calls_out': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'emails_in': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'emails_out': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'phone_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Phone']", 'symmetrical': 'False'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '60', 'primary_key': 'True'}),
            'sms_in': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'sms_number': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sms_participant'", 'null': 'True', 'to': "orm['app.Phone']"}),
            'sms_out': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'})
        },
        'app.interventionparticipantproblem': {
            'Meta': {'object_name': 'InterventionParticipantProblem'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.InterventionParticipant']"}),
            'problem': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'app.phone': {
            'Meta': {'object_name': 'Phone'},
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'})
        }
    }

    complete_apps = ['app']