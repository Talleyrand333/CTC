frappe.listview_settings['Queue'] = {
    add_fields: ["status","ctc_lab_test" ],
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
            return __('Update Queue');
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
                    if(r.message==1){
						cur_list.refresh()
                        frappe.show_alert({
                            message:__('Queue list has been updated.'),
                            indicator:'green'
                        }, 5);
                    }
                },
                error: (r) => {
                    // on error
                }
            })
        }
    }
}