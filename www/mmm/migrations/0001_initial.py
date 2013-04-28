# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'mmm_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'mmm', ['User'])

        # Adding M2M table for field groups on 'User'
        db.create_table(u'mmm_user_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'mmm.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'mmm_user_groups', ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        db.create_table(u'mmm_user_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'mmm.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'mmm_user_user_permissions', ['user_id', 'permission_id'])

        # Adding model 'OfferPageSale'
        db.create_table(u'mmm_offerpagesale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Sale'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price_comment', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal(u'mmm', ['OfferPageSale'])

        # Adding model 'OfferPage'
        db.create_table(u'mmm_offerpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('sale_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sale_1', to=orm['mmm.OfferPageSale'])),
            ('sale_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sale_2', to=orm['mmm.OfferPageSale'])),
            ('sale_3', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sale_3', to=orm['mmm.OfferPageSale'])),
            ('hurry_text', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'mmm', ['OfferPage'])

        # Adding model 'Newsletter'
        db.create_table(u'mmm_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'mmm', ['Newsletter'])

        # Adding model 'ContactMessage'
        db.create_table(u'mmm_contactmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('command', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'mmm', ['ContactMessage'])

        # Adding model 'PasswordRecovery'
        db.create_table(u'mmm_passwordrecovery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mmm.User'])),
            ('secret', self.gf('django.db.models.fields.CharField')(default='51f9b3754af22ff5e7ed6db6f60ffe', max_length=32)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip_addr', self.gf('django.db.models.fields.GenericIPAddressField')(default=None, max_length=39, null=True, blank=True)),
        ))
        db.send_create_signal(u'mmm', ['PasswordRecovery'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'mmm_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table('mmm_user_groups')

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table('mmm_user_user_permissions')

        # Deleting model 'OfferPageSale'
        db.delete_table(u'mmm_offerpagesale')

        # Deleting model 'OfferPage'
        db.delete_table(u'mmm_offerpage')

        # Deleting model 'Newsletter'
        db.delete_table(u'mmm_newsletter')

        # Deleting model 'ContactMessage'
        db.delete_table(u'mmm_contactmessage')

        # Deleting model 'PasswordRecovery'
        db.delete_table(u'mmm_passwordrecovery')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'emarket.sale': {
            'Meta': {'object_name': 'Sale'},
            'begin': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stockmgmt.Product']"}),
            'shopping_cart_description': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'mmm.contactmessage': {
            'Meta': {'object_name': 'ContactMessage'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'mmm.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'mmm.offerpage': {
            'Meta': {'object_name': 'OfferPage'},
            'date_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'hurry_text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sale_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sale_1'", 'to': u"orm['mmm.OfferPageSale']"}),
            'sale_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sale_2'", 'to': u"orm['mmm.OfferPageSale']"}),
            'sale_3': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sale_3'", 'to': u"orm['mmm.OfferPageSale']"})
        },
        u'mmm.offerpagesale': {
            'Meta': {'object_name': 'OfferPageSale'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_comment': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Sale']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'mmm.passwordrecovery': {
            'Meta': {'object_name': 'PasswordRecovery'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.GenericIPAddressField', [], {'default': 'None', 'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'29f98c91778bfedace0a838243e20d'", 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mmm.User']"})
        },
        u'mmm.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'stockmgmt.product': {
            'Meta': {'object_name': 'Product'},
            'article_family': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'deliverable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ean': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['stockmgmt.ProductType']", 'null': 'True', 'blank': 'True'}),
            'public_price': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['stockmgmt.Supplier']", 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'stockmgmt.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'shortcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'})
        },
        u'stockmgmt.supplier': {
            'Meta': {'object_name': 'Supplier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['mmm']