# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Supplier'
        db.create_table(u'stockmgmt_supplier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'stockmgmt', ['Supplier'])

        # Adding model 'ProductType'
        db.create_table(u'stockmgmt_producttype', (
            ('shortcode', self.gf('django.db.models.fields.CharField')(max_length=16, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal(u'stockmgmt', ['ProductType'])

        # Adding model 'Product'
        db.create_table(u'stockmgmt_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['stockmgmt.ProductType'], null=True, blank=True)),
            ('article_family', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['stockmgmt.Supplier'], null=True, blank=True)),
            ('public_price', self.gf('django.db.models.fields.DecimalField')(default=None, null=True, max_digits=6, decimal_places=2, blank=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('ean', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal(u'stockmgmt', ['Product'])

        # Adding model 'Package'
        db.create_table(u'stockmgmt_package', (
            (u'product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stockmgmt.Product'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'stockmgmt', ['Package'])

        # Adding M2M table for field products on 'Package'
        db.create_table(u'stockmgmt_package_products', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm[u'stockmgmt.package'], null=False)),
            ('product', models.ForeignKey(orm[u'stockmgmt.product'], null=False))
        ))
        db.create_unique(u'stockmgmt_package_products', ['package_id', 'product_id'])

        # Adding model 'StockMvt'
        db.create_table(u'stockmgmt_stockmvt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockmgmt.Product'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'stockmgmt', ['StockMvt'])


    def backwards(self, orm):
        # Deleting model 'Supplier'
        db.delete_table(u'stockmgmt_supplier')

        # Deleting model 'ProductType'
        db.delete_table(u'stockmgmt_producttype')

        # Deleting model 'Product'
        db.delete_table(u'stockmgmt_product')

        # Deleting model 'Package'
        db.delete_table(u'stockmgmt_package')

        # Removing M2M table for field products on 'Package'
        db.delete_table('stockmgmt_package_products')

        # Deleting model 'StockMvt'
        db.delete_table(u'stockmgmt_stockmvt')


    models = {
        u'stockmgmt.package': {
            'Meta': {'object_name': 'Package', '_ormbases': [u'stockmgmt.Product']},
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stockmgmt.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'products'", 'blank': 'True', 'to': u"orm['stockmgmt.Product']"})
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