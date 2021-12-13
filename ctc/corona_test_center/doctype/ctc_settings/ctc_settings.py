# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CTCSettings(Document):
	

	def validate(self):
		for location in self.ctc_location:
			self.check_series(location)

	def check_series(self,doc):
		abbr = doc.abbreviation
		series_no = doc.series_start
		
		#ceck if series exist:
		if frappe.db.sql("""SELECT `current` FROM `tabSeries` WHERE `name`=%s""", (abbr,)):
			#check if current series number is less than series start
			current = frappe.db.sql("SELECT `current` FROM `tabSeries` WHERE `name`=%s", (abbr,))[0][0]
			if int(current) < series_no:
				#update current_Series_number
				frappe.db.sql("UPDATE `tabSeries` SET `current` = %s WHERE `name`=%s", (series_no ,abbr))
		else:
			frappe.db.sql("INSERT INTO `tabSeries` (`name`, `current`) VALUES (%s, %s)", (abbr,series_no))
		
		frappe.db.commit()