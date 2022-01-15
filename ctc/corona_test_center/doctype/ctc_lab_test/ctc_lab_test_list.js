frappe.listview_settings['CTC Lab Test'] = {
	add_fields: ["status","patient" ],
	get_indicator: function(doc) {
		var colors = {
            "Draft": "red",
			"Tested": "blue",
			"Submitted": "blue",
            "Cancelled": "grey",
			"In Progress": "yellow",
			"Picked Up": "green",
			"Ready To Pick Up": "orange",
		};
		return [__(doc.status), colors[doc.status], "status,=," + doc.status];
	},
	button: {
        show: function(doc) {
            return true;
        },
        get_label: function() {
            return __('Change Status');
        },
        get_description: function(doc) {
            return  ('Print {0}', [doc.name])
        },
        action: function(doc) {
            let dt= doc.doctype
            let dn= doc.name
            frappe.call({
				async:false,
                method: 'ctc.app.test',
                args: {
                    name:doc.name
                },
                callback: (r) => {
                },
                error: (r) => {
                    // on error
                }
            })
        }
    }
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