# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt

from frappe import _
import frappe
from frappe.model.document import Document
from six import string_types
import json,datetime
from frappe.utils import get_datetime
from ctc.utils import generate_random
class CTCPatient(Document):

	def validate(self):
		self.full_name = ' '.join(filter(lambda x: x, [self.first_name, self.last_name]))
		self.validate_zip_code()
		self.validate_country_code()
		self.check_duplicate()
		#self.create_labtest()
		self.set_subscription_status()
		#self.id_number = generate_random()
	
	def set_subscription_status(self):
		import datetime
		active = False
		existing_subs = frappe.get_all("Patient Subscription",{'patient':self.name},['start_date','end_date'])
		today = datetime.datetime.now()
		if existing_subs:
			for each in existing_subs:
				if get_datetime(each['start_date']) <= today and get_datetime(each['end_date']) > today:
					active = True
		self.active_subscription = "Active" if active else "Inactive"
	
	def check_duplicate(self):
		if not self.is_new():return
		conditions = ""
		if self.first_name:				 
			conditions += " WHERE first_name='%s'" %self.first_name
		if self.last_name:
			conditions += " AND last_name= '%s'" %self.last_name
		if self.date_of_birth:
			conditions += " AND date_of_birth= '%s'" %self.date_of_birth
		# if self.phone_number:
		# 	conditions += " AND phone_number= '%s'" %self.phone_number
		

		result = frappe.db.sql(""" SELECT name from `tabCTC Patient` {conditions} """.format(conditions=conditions),as_dict=1)
		print(result)
		if result:
			frappe.throw('Duplicate Patient please check details')

	def autoname(self):
		self.full_name = ' '.join(filter(lambda x: x, [self.first_name, self.last_name]))
		count = 0
		propose=self.full_name
		while frappe.db.exists("CTC Patient",propose):
			count+=1
			propose=self.full_name+f"-{count}"
		self.name=propose
		frappe.db.commit()
		

	
	def create_labtest(self):
		if self.create_lab_test and self.is_new():
			if not self.name:
				self.autoname()
			patient_doc = {
				'doctype':'CTC Lab Test',
				'patient':self.name,
				'test_name':self.test_name,
				'appointment':self.appointment,
				'report_preference':self.report_preference,
				'location':self.location,
				'intro_email_sent':0,
				'full_name':self.full_name,
				'email':self.email,
				'date_of_birth':self.date_of_birth,
				'phone_number':self.phone_number,
				'town':self.towncity,
				'zipcode':self.zip_code,
				'street_number':self.street_number,
				'street':self.street
			}
			doc = frappe.get_doc(patient_doc)
			doc.save()
			frappe.msgprint(_(f"Lab Test {doc.name} created!"))
			
	

	def validate_zip_code(self):
		value = self.zip_code.strip()
		for each in value:
			if not each.isdigit():
				frappe.throw("Zipcode must be made up of numbers")
		if len(value)!=5:
			frappe.throw(_("Zipcode must be 5 characters"))


	def validate_country_code(self):
		if '+49' not in self.phone_number.split(" "):
			if not self.phone_number[0]=="+":
				self.phone_number = "+49 "+self.phone_number

			
			


	

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
			
