# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from six import string_types
import json,datetime

class PatientCTC(Document):
	pass

	def validate(self):
		self.full_name = ' '.join(filter(lambda x: x, [self.first_name, self.last_name]))


	

@frappe.whitelist(allow_guest=True, xss_safe=True)
def create_patient_appointment(data):
	#Create the custom doctypes from api object received.
	if isinstance(data,string_types):
		data = json.loads(data)
	patient_dict = {
		'doctype':"Patient CTC",
		'first_name':data['first_name'],
		'last_name':data['last_name'],
		'date_of_birth':datetime.datetime.strptime(data['date_of_birth'],'%d.%m.%Y'),
		'email':data['email'] or "",
		'phone_number':data['phone_number'],
		'street':data['street'],
		'towncity':data['towncity'],
		'zip_code':data['zipcode']
	}
	patient_doc = frappe.get_doc(patient_dict)
	patient_doc.save()
	lab_dict = {
		'doctype':"CTC Lab Test",
		'patient':patient_doc.name,
		'status':"Draft",
		'test_name':data['test_name'],
		'report_status':data['report_status'],
		'report_preference':data['report_preference'],
		'location':data['location'],
	}
	lab_doc= frappe.get_doc(lab_dict)
	lab_doc.save()
	return(lab_doc.name)
		    
