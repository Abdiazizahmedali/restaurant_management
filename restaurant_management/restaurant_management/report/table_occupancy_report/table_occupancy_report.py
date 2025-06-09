# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Table No"),
			"fieldname": "table_no",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Table Name"),
			"fieldname": "table_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Seating Capacity"),
			"fieldname": "seating_capacity",
			"fieldtype": "Int",
			"width": 120
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Location"),
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Table Type"),
			"fieldname": "table_type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Current Order"),
			"fieldname": "current_order",
			"fieldtype": "Link",
			"options": "Restaurant Order",
			"width": 150
		},
		{
			"label": _("Order Time"),
			"fieldname": "order_time",
			"fieldtype": "Datetime",
			"width": 150
		},
		{
			"label": _("Customer"),
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 150
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	
	return frappe.db.sql(f"""
		SELECT 
			t.table_no,
			t.table_name,
			t.seating_capacity,
			t.status,
			t.location,
			t.table_type,
			o.name as current_order,
			o.order_time,
			o.customer_name
		FROM `tabRestaurant Table` t
		LEFT JOIN `tabRestaurant Order` o ON t.name = o.table 
			AND o.status NOT IN ('Paid', 'Cancelled')
			AND o.docstatus = 1
		WHERE t.is_active = 1 {conditions}
		ORDER BY t.table_no
	""", filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	
	if filters.get("status"):
		conditions += " AND t.status = %(status)s"
	
	if filters.get("table_type"):
		conditions += " AND t.table_type = %(table_type)s"
	
	if filters.get("location"):
		conditions += " AND t.location = %(location)s"
	
	return conditions