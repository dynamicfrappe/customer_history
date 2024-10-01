// Copyright (c) 2024, customer_history and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment of Obligations', {
	refresh : function(frm){
        frm.set_query("commitment_number", () => {
            return { filters: {"residual": [">", 0]} };
        });
    },
});
