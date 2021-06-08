# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt
import datetime,json
import frappe
from frappe import _
from frappe.model.document import Document
from six import string_types
import pytz

class CTCLabTest(Document):

	def validate(self):
		if self._action=='submit':
			self.status ="Tested"
		
	
	def on_cancel(self):
		self.status = "Cancelled"


	def before_submit(self):
		self.fetch_date()
		self.set_appointment_end()
		
	

	def set_appointment_end(self):
		from frappe.utils import get_datetime
		if self.appointment:
			appointment_end = get_datetime(self.appointment) + datetime.timedelta(minutes=5)
			self.appointment_end=appointment_end

	

	def fetch_date(self):
		#Crude implementation
		tz = pytz.timezone('Europe/Berlin')
		now=datetime.datetime.now(tz)
		self.test_time = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
						
@frappe.whitelist()
def send_email_to_patient(doc):
	if isinstance(doc,string_types):
		doc = json.loads(doc)
		doc= frappe.get_doc(doc)
	if doc.report_preference=="Email" and doc.report_status!='Faulty':
		template = frappe.get_doc("CTC Settings")
		if not(template.get('postive_email_template') or template.get('negative_email_template')):
			frappe.throw(_("Please ensure that all template fields in CTC Settings page are field"))
		positive = frappe.get_doc("Email Template",template.positive_email_template).response
		negative = frappe.get_doc("Email Template",template.negative_email_template).response
		data = vars(doc)
		message = positive if doc.report_status =="Positive" else negative
		email_args = {
				"recipients": [doc.email],
				"message": frappe.render_template(message,data),
				"subject": _('Test Results'),
				"attachments": [frappe.attach_print("CTC Lab Test", doc.name)],
				"reference_doctype": doc.doctype,
				"reference_name": doc.name
		}
		frappe.sendmail(recipients=email_args['recipients'],
		message=email_args['message'],
		subject=email_args['subject'],
		attachment=email_args['attachments'],
		reference_doctype=doc.doctype,
		reference_name=doc.name)
		return True
