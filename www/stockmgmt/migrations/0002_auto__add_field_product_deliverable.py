# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.deliverable'
        db.add_column(u'stockmgmt_product', 'deliverable',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.deliverable'
        db.delete_column(u'stockmgmt_product', 'deliverable')


    models = {
        u'stockmgmt.package': {
            'Meta': {'object_name': 'Package', '_ormbases': [u'stockmgmt.Product']},
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stockmgmt.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'products'", 'blank': 'True', 'to': u"orm['stockmgmt.Product']"})
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
        u'stockmgmt.stockmvt': {
            'Meta': {'object_name': 'StockMvt'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stockmgmt.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'stockmgmt.supplier': {
            'Meta': {'object_name': 'Supplier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['stockmgmt']