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
		self.send_email_to_patient()


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
						

	def send_email_to_patient(self):
		if self.report_preference=="Email" and self.report_status!='Faulty':
			negative_msg = f"""Guten Tag, es gibt gute Nachrichten!
					Wie das Testergebnis vom {{ frappe.utils.formatdate(doc.get_formatted('test_time'), "dd.MM.yyyy:HH:mm") }} zeigt, wurde bei Ihnen das Coronavirus nicht nachgewiesen.
					Bleiben Sie gesund! 
					Als Anlage erhalten Sie die Bescheinigung zu Ihrem Testergebnis.

					Ihr CoronaTestPoint Team
					Elmshorner Str.25
					25421 Pinneberg"""

			postive_msg = f"""Guten Tag, es gibt gute Nachrichten!
								Wie das Testergebnis vom {{ frappe.utils.formatdate(doc.get_formatted('test_time'), "dd.MM.yyyy:HH:mm") }} zeigt, wurde bei Ihnen das Coronavirus nicht nachgewiesen.
								Bleiben Sie gesund! 
								Als Anlage erhalten Sie die Bescheinigung zu Ihrem Testergebnis.

								Ihr CoronaTestPoint Team
								Elmshorner Str.25
								25421 Pinneberg"""
			
			message = postive_msg if self.report_status =="Positive" else negative_msg
			email_args = {
					"recipients": [self.email],
					"message": _(message),
					"subject": _('Registration Complete'),
					"attachments": [frappe.attach_print("CTC Lab Test", self.name)],
					"reference_doctype": self.doctype,
					"reference_name": self.name
			}
			frappe.sendmail(recipients=email_args['recipients'],
			message=email_args['message'],
			subject=email_args['subject'],
			reference_doctype=self.doctype,
			reference_name=self.name)

			
		

	@frappe.whitelist()		
	def send_result_email(self):
		frappe.msgprint(_("Email has been sent!"))



	@frappe.whitelist()
	def get_events(start,end,filters=None):
		return frappe.db.sql("""select name ,appointment as start, appointment_end as end from `tabCTC Lab Test` where docstatus =1""",as_dict=1)