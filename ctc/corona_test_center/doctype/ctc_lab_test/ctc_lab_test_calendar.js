// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["CTC Lab Test"] = {
	field_map: {
		"start": "appointment",
		"end": "appointment",
		"id": "name",
		"title": "full_name",
		"allDay": "allDay",
	},
	gantt: true,
	// filters: [
	// 	{
	// 		"fieldtype": "Link",
	// 		"fieldname": "project",
	// 		"options": "Project",
	// 		"label": __("Project")
	// 	}
	// ],
	get_events_method: "frappe.desk.calendar.get_events"
}
