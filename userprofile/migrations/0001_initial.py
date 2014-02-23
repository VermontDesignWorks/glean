# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'userprofile_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address_one', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address_two', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='VT', max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone_type', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('mo_emails_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('preferred_method', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('member_organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['memberorgs.MemOrg'], null=True, blank=True)),
            ('joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('ecfirst_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('eclast_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ecphone', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ecrelationship', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('rsvped', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('attended', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hours', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=4, decimal_places=2)),
            ('accepts_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('unsubscribe_key', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('waiver', self.gf('django.db.models.fields.BooleanField')()),
            ('agreement', self.gf('django.db.models.fields.BooleanField')()),
            ('photo_release', self.gf('django.db.models.fields.BooleanField')()),
            ('opt_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'userprofile', ['Profile'])

        # Adding M2M table for field counties on 'Profile'
        m2m_table_name = db.shorten_name(u'userprofile_profile_counties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'userprofile.profile'], null=False)),
            ('county', models.ForeignKey(orm[u'counties.county'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'county_id'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'userprofile_profile')

        # Removing M2M table for field counties on 'Profile'
        db.delete_table(db.shorten_name(u'userprofile_profile_counties'))


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
            'volunteers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'member_organizations'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'})
        },
        u'userprofile.profile': {
            'Meta': {'object_name': 'Profile'},
            'accepts_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'agreement': ('django.db.models.fields.BooleanField', [], {}),
            'attended': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'counties': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['counties.County']"}),
            'ecfirst_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'eclast_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ecphone': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ecrelationship': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '4', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'member_organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['memberorgs.MemOrg']", 'null': 'True', 'blank': 'True'}),
            'mo_emails_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'opt_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone_type': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'photo_release': ('django.db.models.fields.BooleanField', [], {}),
            'preferred_method': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'rsvped': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'VT'", 'max_length': '2'}),
            'unsubscribe_key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True', 'blank': 'True'}),
            'waiver': ('django.db.models.fields.BooleanField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['userprofile']