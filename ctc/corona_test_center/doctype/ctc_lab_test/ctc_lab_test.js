// Copyright (c) 2021, Talleyrand and contributors
// For license information, please see license.txt

frappe.ui.form.on('CTC Lab Test', {
	
	refresh: function(frm) {
		if ((!frm.is_new()) && (frm.doc.docstatus==1) ) {
			frm.add_custom_button(__("Send Email"),()=>{
				frappe.msgprint("Please this is WIP")
			})
			frm.add_custom_button(__("Send SMS"),()=>{
				var number = frm.doc.phone_number;
				var message = 'Your Test Result ID: ' + frm.doc.name + ' Test Name: ' + frm.doc.test_name + ' and Result :' + frm.doc.report_status + '';
			
				if (!number || !message) {
					frappe.throw(__('Did not send SMS, missing patient mobile number or message content.'));
				}
				frappe.call({
					method: 'frappe.core.doctype.sms_settings.sms_settings.send_sms',
					args: {
						receiver_list: [number],
						msg: message
					},
					callback: function (r) {
						if (r.exc) {
							frappe.msgprint(r.exc);
						} else {
							frm.reload_doc();
						}
					}
				});
			})
		}
		
	}
	
});
