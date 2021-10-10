from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		
		'fieldname': 'patient',
		'transactions': [
			{
				'label': _('Lab Tests'),
 				'items': ['CTC Lab Test'],
			},
			{
				'label': _('Subscriptions'),
 				'items': ['Patient Subscription'],
			},
		]
	}
