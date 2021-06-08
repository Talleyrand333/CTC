frappe.listview_settings['CTC Lab Test'] = {
	add_fields: ["patient",'testname','location','report_status','status'],
	get_indicator: function(doc) {
		var status_color = {
			"Draft": "grey",
			"Tested": "yellow",
            "Submitted":"red",
            'Cancelled':'blue'
           
		};
		return [__(doc.status), status_color[doc.status], "status,=,"+doc.status];
	},
	
};