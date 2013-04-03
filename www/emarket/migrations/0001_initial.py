# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sale'
        db.create_table(u'emarket_sale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('begin', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockmgmt.Product'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('shopping_cart_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'emarket', ['Sale'])

        # Adding model 'Order'
        db.create_table(u'emarket_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exposed_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mmm.User'])),
            ('billing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Address'])),
            ('promo_code', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal(u'emarket', ['Order'])

        # Adding model 'OrderSale'
        db.create_table(u'emarket_ordersale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Order'])),
            ('sale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Sale'])),
            ('delivery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Address'], null=True, blank=True)),
        ))
        db.send_create_signal(u'emarket', ['OrderSale'])

        # Adding model 'Address'
        db.create_table(u'emarket_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('additional', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'emarket', ['Address'])

        # Adding model 'Be2billTransaction'
        db.create_table(u'emarket_be2billtransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Order'])),
            ('_3dsecure', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cardcode', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('cardcountry', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('cardfullname', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('cardtype', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('cardvaliditydate', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('clientemail', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('clientident', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('execcode', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('extradata', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=510, blank=True)),
            ('operationtype', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('transactionid', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('blob', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'emarket', ['Be2billTransaction'])

        # Adding model 'PartnersSubscription'
        db.create_table(u'emarket_partnerssubscription', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Order'], primary_key=True)),
            ('register', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'emarket', ['PartnersSubscription'])


    def backwards(self, orm):
        # Deleting model 'Sale'
        db.delete_table(u'emarket_sale')

        # Deleting model 'Order'
        db.delete_table(u'emarket_order')

        # Deleting model 'OrderSale'
        db.delete_table(u'emarket_ordersale')

        # Deleting model 'Address'
        db.delete_table(u'emarket_address')

        # Deleting model 'Be2billTransaction'
        db.delete_table(u'emarket_be2billtransaction')

        # Deleting model 'PartnersSubscription'
        db.delete_table(u'emarket_partnerssubscription')


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
        u'emarket.address': {
            'Meta': {'object_name': 'Address'},
            'additional': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'emarket.be2billtransaction': {
            'Meta': {'object_name': 'Be2billTransaction'},
            '_3dsecure': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'blob': ('django.db.models.fields.TextField', [], {}),
            'cardcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'cardcountry': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'cardfullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cardtype': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'cardvaliditydate': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'clientemail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'clientident': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'execcode': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'extradata': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '510', 'blank': 'True'}),
            'operationtype': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Order']"}),
            'transactionid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        u'emarket.order': {
            'Meta': {'object_name': 'Order'},
            'billing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Address']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exposed_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'promo_code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mmm.User']"})
        },
        u'emarket.ordersale': {
            'Meta': {'object_name': 'OrderSale'},
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Address']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Order']"}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Sale']"})
        },
        u'emarket.partnerssubscription': {
            'Meta': {'object_name': 'PartnersSubscription'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Order']", 'primary_key': 'True'}),
            'register': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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

    complete_apps = ['emarket']