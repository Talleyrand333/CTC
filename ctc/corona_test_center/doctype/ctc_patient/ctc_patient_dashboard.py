from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		
		'fieldname': 'patient',
		'transactions': [
			{
				'label': _('Appointments and Patient Encounters'),
				'items': ['Patient Appointment']
			},
			{
				'label': _('Lab Tests'),
 				'items': ['CTC Lab Test']
			},
		]
	}
