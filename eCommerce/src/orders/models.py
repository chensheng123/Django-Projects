from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import models

# Create your models here.
from carts.models import Cart
from django.db.models.signals import pre_save


class UserCheckout(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True) #not required
	email = models.EmailField(unique=True) #--> required


	def __unicode__(self): 
		return self.email


ADDRESS_TYPE = (
	('billing', 'billing'),
	('shipping', 'shipping'),
)		

class UserAddress(models.Model):
	user = models.ForeignKey(UserCheckout)
	type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
	street = models.CharField(max_length=120)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=120)
	zipcode = models.CharField(max_length=120)

	def __unicode__(self):
		return self.street


class Order(models.Model):
	cart = models.ForeignKey(Cart)
	user = models.ForeignKey(UserCheckout)
	shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', null=True)
	shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99)
	order_total = models.DecimalField(max_digits=50, decimal_places=2, )
	order_id = models.CharField(max_length=20, null=True, blank=True)


	def __unicode__(self):
		return str(self.cart.id)




def order_pre_save(sender, instance, *args, **kwargs):
	shipping_total_price = instance.shipping_total_price
	cart_total = instance.cart.total
	order_total = Decimal(shipping_total_price) + Decimal(cart_total)
	instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)




























