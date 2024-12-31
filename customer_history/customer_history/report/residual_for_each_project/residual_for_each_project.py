# Copyright (c) 2024, customer_history and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_date()
	return columns, data

def get_date():
	commitment_types = frappe.get_all("Commitment Type" , pluck="name")
	projects = frappe.get_all("Customer Project Name" , pluck="name")
	list = []
	for project in projects :
		dict ={}
		dict["project"] = project
		for commitment_type in commitment_types :
			dict[f"{commitment_type}"] = 0.0
			sql = f''' 
				select 
					sum(residual) as commitment_type 
				from 
					`tabCustomer History`
				where 
					commitment_type = '{commitment_type}'
					and
					project_name = '{project}'
				group by
					project_name
				'''
			customer_history = frappe.db.sql(sql , as_dict = 1)
			if customer_history :
				dict[f"{commitment_type}"] = customer_history[0]["commitment_type"]
		list.append(dict)
	return list


def get_columns():
	columns =[
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options" : "Customer Project Name",
			"width": 150,
		},
	]
	commitment_types = frappe.get_all("Commitment Type" , pluck="name")
	for commitment_type in commitment_types :
		columns.append({
			"label": _(f"{commitment_type}"),
			"fieldname": f"{commitment_type}" ,
			"fieldtype": "Float",
			"width": 150,
		},)
	return columns
		