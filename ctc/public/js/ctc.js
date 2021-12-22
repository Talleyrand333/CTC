frappe.provide('frappe.ui.form');
frappe.provide('ctc');

frappe.ui.form.CTCLabTestsQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
	init: function(doctype, after_insert, init_callback, doc, force) {
		this._super(doctype, after_insert, init_callback, doc, force);
		this.skip_redirect_on_error = true;
	},
	
	render_dialog: function() {
		this.mandatory = this.mandatory.concat(this.get_variant_fields());
		this._super();
	},

	get_variant_fields: function() {
		var variant_fields = [
		{
			label: __("Patient"),
			fieldname: "patient",
			fieldtype: "Link",
            reqd:1
		},
		
		{
			label: __("Location"),
			fieldname: "location",
			fieldtype: "Link",
            reqd:1
		},
		{
			label: __("Report Status"),
			fieldname: "report_status",
			fieldtype: "Select",
            options:['Negative','Postive','Invalid','Pending','Faulty']
		},
		
		{
			label: __("Print On Submit"),
			fieldname: "print_on_submit",
			fieldtype: "Check"
		},
		
		
		{
			label: __("Report Preference"),
			fieldname: "report_preference",
			fieldtype: "Select",
            options:['Email','Print','Sms']
		},
		
		];

		return variant_fields;
        
	},
    register_primary_action: function() {
		var me = this;
		console.log('Hello 1')
		this.dialog.set_primary_action(__('Save'), function() {
            
            var data = me.dialog.get_values();
			if (me.dialog.doc.report_preference=='Print'){
				me.dialog.set_value('print_on_submit',1)
				me.dialog.refresh_fields()
			} else {
				me.dialog.set_value('print_on_submit',0)
				me.dialog.refresh_fields()
			}
            me.insert();
        });
	},
	report_preference:function(){
		console.log('jslsj')
	}
})
