// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["CTC Lab Test"] = {
	field_map: {
		"start": "appointment",
		"end": "appointment_end",
		"id": "name",
		"allDay": "all_day",
		"title": "full_name",
	},
	// style_map: {
	// 	"Public": "success",
	// 	"Private": "info"
	// },
	// get_events_method: "frappe.desk.calendar.get_events"
	get_events_method: "ctc.utils.events.get_events"
}
