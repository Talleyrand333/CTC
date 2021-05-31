# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt
import datetime
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
import pytz

class CTCLabTest(Document):

	def on_submit(self):
		self.status = "Submitted"
	
	def on_cancel(self):
		self.status = "Canceled"
	

	def fetch_date(self):
		#Crude implementation
		tz = pytz.timezone('Europe/Berlin')
		now=datetime.datetime.now(tz)
		self.test_time = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
		

		


	def validate(self):
		self.send_email_to_patient()
		self.fetch_date()
		# if self._action!="submit":
		# 	self.status="Draft"
		# 	if self.is_new():
				# self.send_email_to_patient()
				
			

	def send_email_to_patient(self):
		self.intro_email_sent=0
		self.intro_email_sent=1
		# email_args = {
		# 		"recipients": [self.email],
		# 		"message": _(f"You have been registered for your Lab test. the ID is {self.name}, Please come for the test with this ID "),
		# 		"subject": _('Registration Complete'),
		# 		# "attachments": [frappe.attach_print("CTC Lab Test", self.name)],
		# 		"reference_doctype": self.doctype,
		# 		"reference_name": self.name
		# 		}
		# enqueue(method=frappe.sendmail, queue='short', timeout=300, async=True, **email_args)

		
		

	@frappe.whitelist()		
	def send_result_email(self):
		frappe.msgprint(_("Email has been sent!"))



