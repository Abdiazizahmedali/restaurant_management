# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RestaurantTable(Document):
	def validate(self):
		self.validate_seating_capacity()
		self.validate_table_no()
	
	def validate_seating_capacity(self):
		if self.seating_capacity <= 0:
			frappe.throw("Seating capacity must be greater than 0")
	
	def validate_table_no(self):
		if not self.table_no:
			frappe.throw("Table No is required")
		
		# Check for duplicate table numbers
		existing = frappe.db.exists("Restaurant Table", {
			"table_no": self.table_no,
			"name": ["!=", self.name]
		})
		if existing:
			frappe.throw(f"Table No {self.table_no} already exists")
	
	def on_update(self):
		# Update any active orders if table status changes
		if self.has_value_changed("status"):
			self.update_table_orders()
	
	def update_table_orders(self):
		if self.status == "Out of Service":
			# Cancel any pending orders for this table
			orders = frappe.get_all("Restaurant Order", 
				filters={
					"table": self.name,
					"status": ["in", ["Draft", "Submitted", "Preparing"]]
				}
			)
			for order in orders:
				order_doc = frappe.get_doc("Restaurant Order", order.name)
				order_doc.add_comment("Comment", f"Table {self.table_no} is out of service")
	
	@frappe.whitelist()
	def set_occupied(self):
		self.status = "Occupied"
		self.save()
		return self.status
	
	@frappe.whitelist()
	def set_available(self):
		self.status = "Available"
		self.save()
		return self.status
	
	@frappe.whitelist()
	def reserve_table(self):
		if self.status != "Available":
			frappe.throw(f"Table {self.table_no} is not available for reservation")
		self.status = "Reserved"
		self.save()
		return self.status

@frappe.whitelist()
def get_available_tables():
	"""Get all available tables"""
	return frappe.get_all("Restaurant Table", 
		filters={"status": "Available", "is_active": 1},
		fields=["name", "table_no", "seating_capacity", "location", "table_type"]
	)

@frappe.whitelist()
def get_table_status_summary():
	"""Get summary of table statuses"""
	return frappe.db.sql("""
		SELECT status, COUNT(*) as count
		FROM `tabRestaurant Table`
		WHERE is_active = 1
		GROUP BY status
	""", as_dict=True)