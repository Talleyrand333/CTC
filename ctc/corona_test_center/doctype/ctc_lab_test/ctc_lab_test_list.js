frappe.listview_settings['CTC Lab Test'] = {
	add_fields: ["patient",'testname','location','report_status','status'],
	get_indicator: function(doc) {
		var status_color = {
			"Draft": "grey",
			"Tested": "yellow",
            'Cancelled':'blue',
           
		};
		return [__(doc.status), status_color[doc.status], "status,=,"+doc.status];
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

