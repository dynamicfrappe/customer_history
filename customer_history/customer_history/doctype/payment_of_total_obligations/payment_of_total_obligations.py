# Copyright (c) 2024, customer_history and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now
from frappe.model.document import Document

class PaymentofTotalObligations(Document):
    def before_save(self):
        # self.calculate_residual()
        self.validate_commitment_amount()

    def before_submit(self):
        self.append_payment_of_obligations()

    def validate_commitment_amount(self):
        sum = 0 
        for commitment in self.commitments :
            if commitment.payment_amount :
                sum += commitment.payment_amount
        if self.amount != sum :
            frappe.throw(_("Amount of payment of total obligations not equal total of commitment amount "))


    # def calculate_residual(self):
    #     for commitment in self.commitments :
    #         customer_history = frappe.get_doc("Customer History" , commitment.commitment)
    #         residual_before = customer_history.payment_amount - customer_history.total_commitment_amount 
    #         residual_after = customer_history.payment_amount - customer_history.total_commitment_amount - commitment.payment_amount
    #         if residual_after < 0 :
    #             frappe.throw(_(f"The residual should pay {residual_before} only"))
    #         commitment.residual = residual_after
            
    def append_payment_of_obligations(self):
        for commitment in self.commitments :
            if commitment.commitment :        
                customer_history = frappe.get_doc("Customer History" , commitment.commitment)
                customer_history.append("commitment" , {
                        "voucher_type" : self.doctype ,
				        "voucher_no" : self.name,
                        "commitment_amount" :commitment.payment_amount , 
                        "commitment_date" : now()
                })
                customer_history.total_commitment_amount += commitment.payment_amount
                customer_history.save()

    @frappe.whitelist()
    def get_customer_history(self , project):
        customers = frappe.get_all("Customer History" , filters = {"project_name" : project} , pluck="name")
        for customer in customers :
            customer = frappe.get_doc("Customer History"  , customer)
            self.append("commitments",{
                "commitment" : customer.name,
                "commitment_amount" : customer.payment_amount,
                "residual" : customer.residual
            })

