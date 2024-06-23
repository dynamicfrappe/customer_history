// Copyright (c) 2024, customer_history and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Payment of Total Obligations', {
// 	get: function(frm) {
// 		let d = new frappe.ui.Dialog({
// 			title: "Enter details",
// 			fields: [
// 			  {
// 				label: "Project",
// 				fieldname: "project",
// 				fieldtype: "Link",
// 				options : "Customer Project Name"
// 			  },
// 			  {
// 				label: "Beneficiary",
// 				fieldname: "beneficiary",
// 				fieldtype: "Link",
// 				options: "Beneficiary"
// 			 }
// 			],
// 			primary_action_label: "Submit",
// 			primary_action(values) {
// 				console.log(values.project)
// 				frm.call({
// 					doc: frm.doc,
// 					method: "get_customer_history",
// 					args: {project : values.project,
// 						beneficiary:values.beneficiary
// 					},
// 					callback: function (r) {
// 						frm.refresh_field('commitments')
// 					},
// 				});
// 			  d.hide();
// 			},
// 		  });
// 		  frappe
// 		  d.show();	}
	  
// });
frappe.ui.form.on('Payment of Total Obligations', {
    get: function(frm) {
        let d = new frappe.ui.Dialog({
            title: "Enter details",
            fields: [
                {
                    label: "Project",
                    fieldname: "project",
                    fieldtype: "Link",
                    options: "Customer Project Name",
                },
                {
                    label: "Beneficiary",
                    fieldname: "beneficiary",
                    fieldtype: "Link",
                    options: "Beneficiary"
                }
            ],
            primary_action_label: "Submit",
            primary_action(values) {
                frm.call({
                    doc: frm.doc,
                    method: "get_customer_history",
                    args: {
                        project: values.project,
                        beneficiary: values.beneficiary
                    },
                    callback: function(r) {
                        let totalResidual = 0;
						let totalCommitmentAmount = 0;
						let amount = frm.doc.amount;
                        if (frm.doc.commitments && frm.doc.commitments.length > 0) {
                            frm.doc.commitments.forEach(function(row) {
                                totalResidual += row.residual || 0;
                            });
                        }
						if (frm.doc.commitments && frm.doc.commitments.length > 0) {
                            frm.doc.commitments.forEach(function(row) {
                                totalCommitmentAmount += row.commitment_amount || 0;
                            });
                        }
                        frm.set_value('total_residual', totalResidual);
						frm.set_value('total_commitment_amount', totalCommitmentAmount);
						frm.set_value('difference',amount)
						frm.refresh_field('total_commitment_amount');
                        frm.refresh_field('total_residual');
						frm.refresh_field('commitments');
						frm.refresh_field('difference');
                    }
                });
                d.hide();
            },
        });
        d.show();
    }
});
frappe.ui.form.on('Commitment Number', {
    payment_amount: function(frm) {
        calculateTotalPayment(frm);
    }
});

function calculateTotalPayment(frm) {
    let totalPayment = 0;
    if (frm.doc.commitments && frm.doc.commitments.length > 0) {
        frm.doc.commitments.forEach(function(row) {
            totalPayment += row.payment_amount || 0;
        });
    }
    frm.set_value('total_payment_amount', totalPayment);
    frm.refresh_field('total_payment_amount');
    if (frm.doc.amount !== undefined && frm.doc.amount !== null) {
        let difference = frm.doc.amount - totalPayment;
        frm.set_value('difference', difference);
        frm.refresh_field('difference');
    }
}







