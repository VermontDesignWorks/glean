# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Profile.phone_type'
        db.alter_column(u'userprofile_profile', 'phone_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True))

        # Changing field 'Profile.city'
        db.alter_column(u'userprofile_profile', 'city', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Profile.ecphone'
        db.alter_column(u'userprofile_profile', 'ecphone', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Profile.state'
        db.alter_column(u'userprofile_profile', 'state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'Profile.ecrelationship'
        db.alter_column(u'userprofile_profile', 'ecrelationship', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Profile.attended'
        db.alter_column(u'userprofile_profile', 'attended', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Profile.phone'
        db.alter_column(u'userprofile_profile', 'phone', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Profile.eclast_name'
        db.alter_column(u'userprofile_profile', 'eclast_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Profile.rsvped'
        db.alter_column(u'userprofile_profile', 'rsvped', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Profile.ecfirst_name'
        db.alter_column(u'userprofile_profile', 'ecfirst_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Profile.age'
        db.alter_column(u'userprofile_profile', 'age', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Profile.preferred_method'
        db.alter_column(u'userprofile_profile', 'preferred_method', self.gf('django.db.models.fields.CharField')(max_length=1, null=True))

    def backwards(self, orm):

        # Changing field 'Profile.phone_type'
        db.alter_column(u'userprofile_profile', 'phone_type', self.gf('django.db.models.fields.CharField')(max_length=1))

        # Changing field 'Profile.city'
        db.alter_column(u'userprofile_profile', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Profile.ecphone'
        db.alter_column(u'userprofile_profile', 'ecphone', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Profile.state'
        db.alter_column(u'userprofile_profile', 'state', self.gf('django.db.models.fields.CharField')(max_length=2))

        # Changing field 'Profile.ecrelationship'
        db.alter_column(u'userprofile_profile', 'ecrelationship', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Profile.attended'
        db.alter_column(u'userprofile_profile', 'attended', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Profile.phone'
        db.alter_column(u'userprofile_profile', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Profile.eclast_name'
        db.alter_column(u'userprofile_profile', 'eclast_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Profile.rsvped'
        db.alter_column(u'userprofile_profile', 'rsvped', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Profile.ecfirst_name'
        db.alter_column(u'userprofile_profile', 'ecfirst_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Profile.age'
        db.alter_column(u'userprofile_profile', 'age', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Profile.preferred_method'
        db.alter_column(u'userprofile_profile', 'preferred_method', self.gf('django.db.models.fields.CharField')(max_length=1))

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
        u'memberorgs.memorg': {
            'Meta': {'object_name': 'MemOrg'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'muted'", 'max_length': '20'}),
            'counties': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_organizations'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['counties.County']"}),
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
            'testing_email': ('django.db.models.fields.CharField', [], {'max_length': "'200'", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'})
        },
        u'userprofile.profile': {
            'Meta': {'object_name': 'Profile'},
            'accepts_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'agreement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attended': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'counties': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['counties.County']"}),
            'ecfirst_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'eclast_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'ecphone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'ecrelationship': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'member_organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['memberorgs.MemOrg']", 'null': 'True', 'blank': 'True'}),
            'mo_emails_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'not_notified': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opt_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'phone_type': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1', 'null': 'True'}),
            'photo_release': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'preferred_method': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1', 'null': 'True'}),
            'rsvped': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'VT'", 'max_length': '2', 'null': 'True'}),
            'tasks_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tasks_delivery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tasks_farm_pickups': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tasks_gleaning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tasks_processing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unsubscribe_key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'waiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['userprofile']