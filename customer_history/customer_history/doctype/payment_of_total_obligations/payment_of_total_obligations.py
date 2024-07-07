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
        self.calculate_number_of_commitments()
        # self.validatees()

    def before_submit(self):
        self.append_payment_of_obligations()

    def validate_commitment_amount(self):
        sum = 0 
        for commitment in self.commitments :
            if commitment.payment_amount :
                sum += commitment.payment_amount
        if self.amount != sum :
            frappe.throw(_("Amount of payment of total obligations not equal total of commitment amount "))
    def validatees(self):
        total_payment = 0
        total_commitment = 0
        total_residual = 0

        for commitment in self.commitments:
            if  commitment.payment_amount:
                total_payment += commitment.payment_amount
            if commitment.commitment_amount:
                total_commitment += commitment.commitment_amount
            if commitment.residual:
                total_residual += commitment.residual    

        self.total_payment_amount = total_payment
        self.total_commitment_amount = total_commitment
        self.total_residual = total_residual

    def calculate_number_of_commitments(self):
        for commitment in self.commitments :
            self.number_of_commitments =commitment.idx



           


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
    def get_customer_history(self, project, beneficiary=None,sector=None,commitment_type=None):
        filters = {"project_name": project}
        if beneficiary:
            filters["beneficiary"] = beneficiary
        if sector:
            filters["sector"] = sector
        if commitment_type:
           filters["commitment_type"] = commitment_type         
        
        customers = frappe.get_all("Customer History", filters=filters, pluck="name")
        for customer in customers:
            customer = frappe.get_doc("Customer History", customer)
            self.append("commitments", {
                "commitment": customer.name,
                "commitment_amount": customer.payment_amount,
                "residual": customer.residual,
                "beneficiary": customer.beneficiary,
                "project": customer.project_name
            })


# @frappe.whitelist()            
# def validatees(doc, method):
#         total_payment = 0
#         total_commitment = 0
#         total_residual = 0

#         for commitment in doc.commitments:
#             if  commitment.payment_amount:
#                 total_payment += commitment.payment_amount
#             if commitment.commitment_amount:
#                 total_commitment += commitment.commitment_amount
#             if commitment.residual:
#                 total_residual += commitment.residual    

#         doc.total_payment_amount = total_payment
#         doc.total_commitment_amount = total_commitment
#         doc.total_residual = total_residual
#         doc.difference = total_payment - doc.amount 