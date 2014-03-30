# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Farm'
        db.create_table(u'farms_farm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address_one', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('address_two', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='VT', max_length=2, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('physical_is_mailing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mailing_address_one', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mailing_address_two', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mailing_city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mailing_state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('mailing_zip', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('phone_1', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone_1_type', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('phone_2', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone_2_type', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('directions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('instructions', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'farms', ['Farm'])

        # Adding M2M table for field farmers on 'Farm'
        m2m_table_name = db.shorten_name(u'farms_farm_farmers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farm', models.ForeignKey(orm[u'farms.farm'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['farm_id', 'user_id'])

        # Adding M2M table for field counties on 'Farm'
        m2m_table_name = db.shorten_name(u'farms_farm_counties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farm', models.ForeignKey(orm[u'farms.farm'], null=False)),
            ('county', models.ForeignKey(orm[u'counties.county'], null=False))
        ))
        db.create_unique(m2m_table_name, ['farm_id', 'county_id'])

        # Adding M2M table for field member_organization on 'Farm'
        m2m_table_name = db.shorten_name(u'farms_farm_member_organization')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farm', models.ForeignKey(orm[u'farms.farm'], null=False)),
            ('memorg', models.ForeignKey(orm[u'memberorgs.memorg'], null=False))
        ))
        db.create_unique(m2m_table_name, ['farm_id', 'memorg_id'])

        # Adding model 'FarmLocation'
        db.create_table(u'farms_farmlocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('farm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farms.Farm'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('directions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('instructions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address_one', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('address_two', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='VT', max_length=2, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('physical_is_mailing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mailing_address_one', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mailing_address_two', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mailing_city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mailing_state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('mailing_zip', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
        ))
        db.send_create_signal(u'farms', ['FarmLocation'])

        # Adding M2M table for field counties on 'FarmLocation'
        m2m_table_name = db.shorten_name(u'farms_farmlocation_counties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farmlocation', models.ForeignKey(orm[u'farms.farmlocation'], null=False)),
            ('county', models.ForeignKey(orm[u'counties.county'], null=False))
        ))
        db.create_unique(m2m_table_name, ['farmlocation_id', 'county_id'])

        # Adding model 'Contact'
        db.create_table(u'farms_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('farm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farms.Farm'], null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('phone_type', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('glean_contact', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('preferred', self.gf('django.db.models.fields.CharField')(default='1', max_length=1, blank=True)),
        ))
        db.send_create_signal(u'farms', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'Farm'
        db.delete_table(u'farms_farm')

        # Removing M2M table for field farmers on 'Farm'
        db.delete_table(db.shorten_name(u'farms_farm_farmers'))

        # Removing M2M table for field counties on 'Farm'
        db.delete_table(db.shorten_name(u'farms_farm_counties'))

        # Removing M2M table for field member_organization on 'Farm'
        db.delete_table(db.shorten_name(u'farms_farm_member_organization'))

        # Deleting model 'FarmLocation'
        db.delete_table(u'farms_farmlocation')

        # Removing M2M table for field counties on 'FarmLocation'
        db.delete_table(db.shorten_name(u'farms_farmlocation_counties'))

        # Deleting model 'Contact'
        db.delete_table(u'farms_contact')


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
        u'farms.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'farm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farms.Farm']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'glean_contact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'phone_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'preferred': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
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

    complete_apps = ['farms']