// Copyright (c) 2021, Talleyrand and contributors
// For license information, please see license.txt

frappe.ui.form.on('CTC Settings', {
	// refresh: function(frm) {

	// }
	default_email_sender:function(){
		//get email_id of email sender
		frappe.call({
			method:'get_email_id',
			doc:cur_frm.doc,
			args:{
				sender:cur_frm.doc.default_email_sender
			},
			callback:function(message){
				if (message){
					cur_frm.set_value('email_id',message['message'])
					cur_frm.refresh_field('email_id')
					cur_frm.refresh_fields()
				}
			}
		})
	}
});
