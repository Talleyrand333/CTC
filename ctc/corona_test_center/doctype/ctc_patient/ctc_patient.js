// Copyright (c) 2021, Talleyrand and contributors
// For license information, please see license.txt

frappe.ui.form.on('CTC Patient', {
	setup: function(frm){
		if(frm.is_new()){
			var d = new Date("January 1, 1990 00:00:00");
			frm.doc.date_of_birth = d
			frm.doc.phone_number = '+49 '
		}
		else{
			frm.set_df_property('create_lab_test','hidden',1);
			frm.set_df_property('appointment','hidden',1);
		}
	},
	refresh:function(frm){
		if(!frm.is_new()){
			frm.set_df_property('create_lab_test','hidden',1);
			frm.set_df_property('appointment','hidden',1);
		}
	}
});
