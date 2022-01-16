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
}