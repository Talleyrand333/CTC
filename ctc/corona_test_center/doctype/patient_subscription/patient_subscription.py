# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import timedelta
from frappe.utils import get_datetime
class PatientSubscription(Document):
	

	def validate(self):
		days = 7 if self.subscription_period == "1 Week" else 30
		self.end_date = get_datetime(self.start_date).date() + timedelta(days=days)

