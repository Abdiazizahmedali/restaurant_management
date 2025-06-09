# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe

def get_context(context):
	# Add custom context for the web form
	context.menu_categories = frappe.get_all("Menu Category", 
		filters={"is_active": 1},
		fields=["name", "category_name", "description", "image"],
		order_by="sort_order"
	)
	
	context.menu_items = frappe.get_all("Item", 
		filters={"is_sales_item": 1, "disabled": 0},
		fields=["name", "item_name", "standard_rate", "item_group", "description", "image"]
	)
	
	context.available_tables = frappe.get_all("Restaurant Table", 
		filters={"status": "Available", "is_active": 1},
		fields=["name", "table_no", "seating_capacity", "location", "table_type"]
	)