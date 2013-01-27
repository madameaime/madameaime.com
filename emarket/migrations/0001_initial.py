# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sale'
        db.create_table('emarket_sale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('begin', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockmgmt.Product'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('emarket', ['Sale'])

        # Adding model 'Order'
        db.create_table('emarket_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exposed_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('billing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Address'])),
        ))
        db.send_create_signal('emarket', ['Order'])

        # Adding model 'OrderSale'
        db.create_table('emarket_ordersale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Order'])),
            ('sale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Sale'])),
            ('delivery', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['emarket.Address'], null=True, blank=True)),
        ))
        db.send_create_signal('emarket', ['OrderSale'])

        # Adding model 'Address'
        db.create_table('emarket_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('additionnal', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=32, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('emarket', ['Address'])

        # Adding model 'ShoppingCartLog'
        db.create_table('emarket_shoppingcartlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emarket.Sale'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['sessions.Session'], null=True, blank=True)),
        ))
        db.send_create_signal('emarket', ['ShoppingCartLog'])


    def backwards(self, orm):
        # Deleting model 'Sale'
        db.delete_table('emarket_sale')

        # Deleting model 'Order'
        db.delete_table('emarket_order')

        # Deleting model 'OrderSale'
        db.delete_table('emarket_ordersale')

        # Deleting model 'Address'
        db.delete_table('emarket_address')

        # Deleting model 'ShoppingCartLog'
        db.delete_table('emarket_shoppingcartlog')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'emarket.address': {
            'Meta': {'object_name': 'Address'},
            'additionnal': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'emarket.order': {
            'Meta': {'object_name': 'Order'},
            'billing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emarket.Address']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exposed_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'emarket.ordersale': {
            'Meta': {'object_name': 'OrderSale'},
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['emarket.Address']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emarket.Order']"}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emarket.Sale']"})
        },
        'emarket.sale': {
            'Meta': {'object_name': 'Sale'},
            'begin': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stockmgmt.Product']"})
        },
        'emarket.shoppingcartlog': {
            'Meta': {'object_name': 'ShoppingCartLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emarket.Sale']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['sessions.Session']", 'null': 'True', 'blank': 'True'})
        },
        'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        },
        'stockmgmt.product': {
            'Meta': {'object_name': 'Product'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['emarket']