# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OrderSale.message'
        db.add_column(u'emarket_ordersale', 'message',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OrderSale.message'
        db.delete_column(u'emarket_ordersale', 'message')


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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
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
            'blob': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cardcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'cardcountry': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'cardfullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cardtype': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'cardvaliditydate': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'clientemail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'clientident': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
        u'emarket.deliveredproduct': {
            'Meta': {'object_name': 'DeliveredProduct'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_sale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.OrderSale']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stockmgmt.Product']"})
        },
        u'emarket.order': {
            'Meta': {'object_name': 'Order'},
            'billing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Address']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exposed_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'promo_code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mmm.User']"})
        },
        u'emarket.ordersale': {
            'Meta': {'object_name': 'OrderSale'},
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emarket.Address']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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

    complete_apps = ['emarket']