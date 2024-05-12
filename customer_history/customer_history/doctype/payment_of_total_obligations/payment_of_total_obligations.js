// Copyright (c) 2024, customer_history and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment of Total Obligations', {
	get: function(frm) {
		let d = new frappe.ui.Dialog({
			title: "Enter details",
			fields: [
			  {
				label: "Project",
				fieldname: "project",
				fieldtype: "Link",
				options : "Customer Project Name"
			  },
			],
			primary_action_label: "Submit",
			primary_action(values) {
				console.log(values.project)
				frm.call({
					doc: frm.doc,
					method: "get_customer_history",
					args: {project : values.project},
					callback: function (r) {
						frm.refresh_field('commitments')
					},
				});
			  d.hide();
			},
		  });
		  d.show();	}
});
