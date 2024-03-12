# For license information, please see license.txt

import frappe
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
		self.residual = customer_history.payment_amount - customer_history.total_commitment_amount - self.payment_amount
	
	def append_payment_of_obligations(self):
		customer_history = frappe.get_doc("Customer History" , self.commitment_number)
		customer_history.append("commitment" , {
				"payment_of_obligations" : self.name,
				"commitment_amount" :self.payment_amount , 
				"commitment_date" : now()
		})
		customer_history.total_commitment_amount += self.payment_amount
		customer_history.save()