# Copyright (c) 2024, customer_history and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class CustomerHistory(Document):
	def before_save(self):
		self.calculate_residual()

	def calculate_residual(self):
		self.residual = self.payment_amount - self.total_commitment_amount
