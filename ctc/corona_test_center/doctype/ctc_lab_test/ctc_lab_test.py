# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt
import datetime
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
import pytz

class CTCLabTest(Document):

	def before_submit(self):
		self.fetch_date()
		self.set_appointment_end()
	

	def set_appointment_end(self):
		from frappe.utils import get_datetime
		if self.appointment:
			appointment_end = get_datetime(self.appointment) + datetime.timedelta(minutes=1)
			self.appointment_end=appointment_end

	

	def fetch_date(self):
		#Crude implementation
		tz = pytz.timezone('Europe/Berlin')
		now=datetime.datetime.now(tz)
		self.test_time = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
						

	def send_email_to_patient(self):
		email_args = {
				"recipients": [self.email],
				"message": _(f"You have been registered for your Lab test. the ID is {self.name}, Please come for the test with this ID "),
				"subject": _('Registration Complete'),
				"attachments": [frappe.attach_print("CTC Lab Test", self.name)],
				"reference_doctype": self.doctype,
				"reference_name": self.name
		}
		enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)

		
		

	@frappe.whitelist()		
	def send_result_email(self):
		frappe.msgprint(_("Email has been sent!"))



	@frappe.whitelist()
	def get_events(start,end,filters=None):
		return frappe.db.sql("""select name ,appointment as start, appointment_end as end from `tabCTC Lab Test` where docstatus =1""",as_dict=1)