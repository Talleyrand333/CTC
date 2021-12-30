frappe.listview_settings['CTC Lab Test'] = {
	add_fields: ["status","patient" ],
	get_indicator: function (doc) {
		if (doc.status === "Draft") {
			// Active
			return [__("Draft"), "gray", "status,=,Draft"];
		} else if (doc.status === "Cancelled") {
			// on hold
			return [__("Cancelled"), "red", "status,=,Cancelled"];
		} else if (doc.status === "On Hold") {
			return [__("On Hold"), "orange", "status,=,On Hold"];
		} else if (doc.status === "Submitted") {
			return [__("Submitted"), "green", "status,=,Submitted"];
		}
	},
}

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

