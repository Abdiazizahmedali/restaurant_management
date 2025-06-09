# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Order ID"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Restaurant Order",
			"width": 120
		},
		{
			"label": _("Customer"),
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Table"),
			"fieldname": "table",
			"fieldtype": "Link",
			"options": "Restaurant Table",
			"width": 100
		},
		{
			"label": _("Order Type"),
			"fieldname": "order_type",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Total Qty"),
			"fieldname": "total_qty",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Total Amount"),
			"fieldname": "total_amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Tax Amount"),
			"fieldname": "tax_amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Grand Total"),
			"fieldname": "grand_total",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Payment Status"),
			"fieldname": "payment_status",
			"fieldtype": "Data",
			"width": 120
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	
	return frappe.db.sql(f"""
		SELECT 
			DATE(creation) as date,
			name,
			customer_name,
			table,
			order_type,
			status,
			total_qty,
			total_amount,
			tax_amount,
			grand_total,
			payment_status
		FROM `tabRestaurant Order`
		WHERE docstatus = 1 {conditions}
		ORDER BY creation DESC
	""", filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	
	if filters.get("from_date"):
		conditions += " AND DATE(creation) >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND DATE(creation) <= %(to_date)s"
	
	if filters.get("order_type"):
		conditions += " AND order_type = %(order_type)s"
	
	if filters.get("status"):
		conditions += " AND status = %(status)s"
	
	if filters.get("table"):
		conditions += " AND table = %(table)s"
	
	return conditions