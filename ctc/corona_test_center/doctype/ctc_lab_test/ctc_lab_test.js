// Copyright (c) 2021, Talleyrand and contributors
// For license information, please see license.txt

frappe.ui.form.on('CTC Lab Test', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			console.log("CALLED")
			frm.add_custom_button(__("Send Email"),()=>{
				console.log("WORKING EMAIL")
			})
			frm.add_custom_button(__("Send SMS"),()=>{
				console.log("WORKING SMS")
			})
		}
		
	}
	
});
