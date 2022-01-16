frappe.listview_settings['Random Doctype'] = {
	add_fields: ["status" ],
	get_indicator: function (doc) {
		if (doc.status === "Tested") {
			// Active
			return [__("Tested"), "orange", "status,=,Tested"];
		} else if (doc.status === "Cancelled") {
			// on hold
			return [__("Cancelled"), "red", "status,=,Cancelled"];
		} else if (doc.status === "On Hold") {
			return [__("On Hold"), "orange", "status,=,On Hold"];
		}
	},
}