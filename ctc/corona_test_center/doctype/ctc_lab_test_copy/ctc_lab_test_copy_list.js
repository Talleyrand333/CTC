frappe.listview_settings['CTC Lab Test Copy'] = {
	add_fields: ['status',],
	get_indicator: function(doc) {
		const status_color = {
			"Draft": "gray",
			"Tested": "yellow",
			"Submitted":"green",
            'Cancelled':'blue',
           
		};
		if (doc.status === "Draft") {
			console.log(doc.status)
			// Active
			return [__("Draft"), "gray", "status,=,Draft"];
		}
		
		return [__(doc.status), status_color[doc.status], "status,=,"+doc.workflow_state];
	},
	// onload: function(){
	// 	console.log(cur_dialog.doc.status)
	// }
	
};

// let old_quick_entry = frappe.ui.form.make_quick_entry;

// let new_quick_entry = (doctype, after_insert, init_callback, doc) => {
// old_quick_entry(doctype, after_insert, init_callback, doc);


// setTimeout(() => {
// 	if (cur_dialog.doc.report_preference == 'Email'){
// 		cur_dialog.set_value('print_on_submit',1)

// 	}
// 	console.log('dialog object is accessible here', cur_dialog);}, 500);
// };


// frappe.ui.form.make_quick_entry = new_quick_entry;
// console.log(cur_dialog,'hello')

