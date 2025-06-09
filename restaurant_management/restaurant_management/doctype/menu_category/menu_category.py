# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MenuCategory(Document):
	def validate(self):
		if not self.sort_order:
			self.sort_order = self.get_next_sort_order()
	
	def get_next_sort_order(self):
		"""Get the next sort order for this category"""
		max_sort_order = frappe.db.sql("""
			SELECT MAX(sort_order) FROM `tabMenu Category`
		""")[0][0] or 0
		return max_sort_order + 1

@frappe.whitelist()
def get_active_categories():
	"""Get all active menu categories"""
	return frappe.get_all("Menu Category", 
		filters={"is_active": 1},
		fields=["name", "category_name", "description", "image"],
		order_by="sort_order"
	)