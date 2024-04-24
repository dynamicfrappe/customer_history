# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now
from frappe.model.document import Document

class PaymentofObligations(Document):
	def before_save(self):
		if self.commitment_number :
			self.calculate_residual()

	def before_submit(self):
		if self.commitment_number :
			self.append_payment_of_obligations()

	def calculate_residual(self):
		customer_history = frappe.get_doc("Customer History" , self.commitment_number)
		residual_before = customer_history.payment_amount - customer_history.total_commitment_amount 
		residual_after = customer_history.payment_amount - customer_history.total_commitment_amount - self.payment_amount
		if residual_after < 0 :
			frappe.throw(_(f"The residual should pay {residual_before} only"))
		self.residual = residual_after

	
	def append_payment_of_obligations(self):
		customer_history = frappe.get_doc("Customer History" , self.commitment_number)
		customer_history.append("commitment" , {
				"voucher_type" : self.doctype ,
				"voucher_no" : self.name,
				"commitment_amount" :self.payment_amount , 
				"commitment_date" : now()
		})
		customer_history.total_commitment_amount += self.payment_amount
		customer_history.save()