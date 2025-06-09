# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, now

class RestaurantOrder(Document):
	def validate(self):
		self.validate_items()
		self.calculate_totals()
		self.validate_table_availability()
		self.set_outstanding_amount()
	
	def validate_items(self):
		if not self.items:
			frappe.throw("Please add at least one item to the order")
		
		for item in self.items:
			if not item.item_code:
				frappe.throw("Item Code is required for all items")
			if flt(item.qty) <= 0:
				frappe.throw(f"Quantity must be greater than 0 for item {item.item_code}")
	
	def calculate_totals(self):
		self.total_qty = 0
		self.total_amount = 0
		
		for item in self.items:
			item.amount = flt(item.rate) * flt(item.qty)
			self.total_qty += flt(item.qty)
			self.total_amount += flt(item.amount)
		
		# Calculate tax
		if self.tax_template:
			self.calculate_taxes()
		else:
			self.tax_amount = 0
		
		self.grand_total = flt(self.total_amount) + flt(self.tax_amount)
	
	def calculate_taxes(self):
		# Simple tax calculation - can be enhanced based on tax template
		tax_rate = frappe.db.get_value("Sales Taxes and Charges Template", 
			self.tax_template, "total_taxes_and_charges") or 0
		self.tax_amount = flt(self.total_amount) * flt(tax_rate) / 100
	
	def validate_table_availability(self):
		if self.order_type == "Dine In" and self.table:
			table_status = frappe.db.get_value("Restaurant Table", self.table, "status")
			if table_status not in ["Available", "Occupied"]:
				frappe.throw(f"Table {self.table} is not available")
	
	def set_outstanding_amount(self):
		self.outstanding_amount = flt(self.grand_total) - flt(self.paid_amount)
		
		if self.outstanding_amount <= 0:
			self.payment_status = "Paid"
		elif self.paid_amount > 0:
			self.payment_status = "Partially Paid"
		else:
			self.payment_status = "Unpaid"
	
	def on_submit(self):
		self.status = "Submitted"
		if self.table and self.order_type == "Dine In":
			# Set table as occupied
			frappe.db.set_value("Restaurant Table", self.table, "status", "Occupied")
		
		# Create stock entries for items if they are stock items
		self.create_stock_entries()
	
	def on_cancel(self):
		self.status = "Cancelled"
		if self.table and self.order_type == "Dine In":
			# Check if there are other active orders for this table
			other_orders = frappe.get_all("Restaurant Order", 
				filters={
					"table": self.table,
					"status": ["not in", ["Cancelled", "Paid"]],
					"name": ["!=", self.name]
				}
			)
			if not other_orders:
				frappe.db.set_value("Restaurant Table", self.table, "status", "Available")
	
	def create_stock_entries(self):
		"""Create stock entries for stock items"""
		for item in self.items:
			item_doc = frappe.get_doc("Item", item.item_code)
			if item_doc.is_stock_item:
				# Create stock entry for consumption
				stock_entry = frappe.new_doc("Stock Entry")
				stock_entry.stock_entry_type = "Material Issue"
				stock_entry.purpose = "Material Issue"
				stock_entry.append("items", {
					"item_code": item.item_code,
					"qty": item.qty,
					"s_warehouse": frappe.db.get_single_value("Stock Settings", "default_warehouse")
				})
				stock_entry.insert()
				stock_entry.submit()
	
	@frappe.whitelist()
	def update_status(self, new_status):
		"""Update order status"""
		allowed_statuses = ["Draft", "Submitted", "Preparing", "Ready", "Served", "Paid", "Cancelled"]
		if new_status not in allowed_statuses:
			frappe.throw(f"Invalid status: {new_status}")
		
		self.status = new_status
		self.save()
		
		# Update table status based on order status
		if self.table and self.order_type == "Dine In":
			if new_status == "Paid":
				# Check if there are other active orders for this table
				other_orders = frappe.get_all("Restaurant Order", 
					filters={
						"table": self.table,
						"status": ["not in", ["Cancelled", "Paid"]],
						"name": ["!=", self.name]
					}
				)
				if not other_orders:
					frappe.db.set_value("Restaurant Table", self.table, "status", "Available")
		
		return self.status
	
	@frappe.whitelist()
	def add_payment(self, amount, payment_method):
		"""Add payment to the order"""
		amount = flt(amount)
		if amount <= 0:
			frappe.throw("Payment amount must be greater than 0")
		
		if amount > self.outstanding_amount:
			frappe.throw("Payment amount cannot be greater than outstanding amount")
		
		self.paid_amount = flt(self.paid_amount) + amount
		self.payment_method = payment_method
		self.set_outstanding_amount()
		
		if self.payment_status == "Paid":
			self.status = "Paid"
		
		self.save()
		
		# Create payment entry
		payment_entry = frappe.new_doc("Payment Entry")
		payment_entry.payment_type = "Receive"
		payment_entry.party_type = "Customer"
		payment_entry.party = self.customer or "Walk-in Customer"
		payment_entry.paid_amount = amount
		payment_entry.received_amount = amount
		payment_entry.reference_no = self.name
		payment_entry.reference_date = frappe.utils.today()
		payment_entry.insert()
		payment_entry.submit()
		
		return self.payment_status

@frappe.whitelist()
def get_menu_items():
	"""Get all menu items for restaurant"""
	return frappe.get_all("Item", 
		filters={"is_sales_item": 1, "disabled": 0},
		fields=["name", "item_name", "standard_rate", "item_group", "description", "image"]
	)

@frappe.whitelist()
def get_order_summary():
	"""Get order summary for dashboard"""
	return frappe.db.sql("""
		SELECT 
			status,
			COUNT(*) as count,
			SUM(grand_total) as total_amount
		FROM `tabRestaurant Order`
		WHERE DATE(creation) = CURDATE()
		GROUP BY status
	""", as_dict=True)