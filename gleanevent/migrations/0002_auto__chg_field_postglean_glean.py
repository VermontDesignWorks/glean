# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PostGlean.glean'
        db.alter_column(u'gleanevent_postglean', 'glean_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gleanevent.GleanEvent'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'PostGlean.glean'
        raise RuntimeError("Cannot reverse this migration. 'PostGlean.glean' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'PostGlean.glean'
        db.alter_column(u'gleanevent_postglean', 'glean_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gleanevent.GleanEvent']))

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'counties.county': {
            'Meta': {'object_name': 'County'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'VT'", 'max_length': '2'}),
            'towns': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'farms.farm': {
            'Meta': {'object_name': 'Farm'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'counties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['counties.County']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'farmers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mailing_address_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_address_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'mailing_zip': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'member_organization': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['memberorgs.MemOrg']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone_1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone_1_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'phone_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone_2_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'physical_is_mailing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'VT'", 'max_length': '2', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'})
        },
        u'farms.farmlocation': {
            'Meta': {'object_name': 'FarmLocation'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'counties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['counties.County']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'farm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farms.Farm']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mailing_address_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_address_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'mailing_zip': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'physical_is_mailing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'VT'", 'max_length': '2', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'})
        },
        u'gleanevent.gleanevent': {
            'Meta': {'object_name': 'GleanEvent'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'attending_volunteers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'attending_voluntters'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'counties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['counties.County']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_by'", 'to': u"orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'farm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farms.Farm']", 'null': 'True', 'blank': 'True'}),
            'farm_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farms.FarmLocation']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'invited_volunteers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'invited_volunteers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'member_organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['memberorgs.MemOrg']", 'blank': 'True'}),
            'not_rsvped': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'not_rsvped'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'officiated_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'officiated_by'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'rsvped': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'rsvped'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'VT'", 'max_length': '2', 'blank': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'time_of_day': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'volunteers_needed': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'waitlist': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'waitlisted'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'})
        },
        u'gleanevent.postglean': {
            'Meta': {'object_name': 'PostGlean'},
            'attended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'glean': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gleanevent.GleanEvent']", 'null': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'memberorgs.memorg': {
            'Meta': {'object_name': 'MemOrg'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'muted'", 'max_length': '20'}),
            'counties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['counties.County']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'mailing_address_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_address_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mailing_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'mailing_zip': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'phone_1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone_1_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'phone_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone_2_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'physical_is_mailing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'VT'", 'max_length': '2', 'blank': 'True'}),
            'testing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'testing_email': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'blank': 'True'}),
            'volunteers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'member_organizations'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gleanevent']