# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt
import datetime
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue

class CTCLabTest(Document):

	def on_submit(self):
		self.status = "Submitted"
	
	def on_cancel(self):
		self.status = "Canceled"

	def validate(self):
		if self._action!="submit":
			self.status="Draft"
			self.test_date = datetime.datetime.date(datetime.datetime.now())
			self.test_time = datetime.datetime.now()
			if self.is_new():
				self.intro_email_sent=0
				self.send_email_to_patient()
				
			

	def send_email_to_patient(self):
		print("HELLOO")
		return
		

	@frappe.whitelist()		
	def send_result_email(self):
		frappe.msgprint(_("Email has been sent!"))



