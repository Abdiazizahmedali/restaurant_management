frappe.ui.form.on('Restaurant Order', {
	refresh: function(frm) {
		// Add custom buttons
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Update Status'), function() {
				show_status_dialog(frm);
			});
			
			if (frm.doc.payment_status !== 'Paid') {
				frm.add_custom_button(__('Add Payment'), function() {
					show_payment_dialog(frm);
				});
			}
			
			if (frm.doc.status === 'Ready') {
				frm.add_custom_button(__('Mark as Served'), function() {
					update_order_status(frm, 'Served');
				});
			}
		}
		
		// Set table filter based on order type
		if (frm.doc.order_type === 'Dine In') {
			frm.set_query('table', function() {
				return {
					filters: {
						'status': ['in', ['Available', 'Occupied']],
						'is_active': 1
					}
				};
			});
		}
	},
	
	order_type: function(frm) {
		if (frm.doc.order_type !== 'Dine In') {
			frm.set_value('table', '');
		}
	},
	
	table: function(frm) {
		if (frm.doc.table) {
			// Get table details
			frappe.db.get_doc('Restaurant Table', frm.doc.table).then(table => {
				if (table.status === 'Occupied' && !frm.doc.name) {
					frappe.msgprint(__('This table is currently occupied'));
				}
			});
		}
	}
});

frappe.ui.form.on('Restaurant Order Item', {
	item_code: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.item_code) {
			frappe.db.get_doc('Item', row.item_code).then(item => {
				frappe.model.set_value(cdt, cdn, 'rate', item.standard_rate);
				calculate_amount(frm, cdt, cdn);
			});
		}
	},
	
	qty: function(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	
	rate: function(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	}
});

function calculate_amount(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	let amount = flt(row.qty) * flt(row.rate);
	frappe.model.set_value(cdt, cdn, 'amount', amount);
}

function show_status_dialog(frm) {
	let dialog = new frappe.ui.Dialog({
		title: __('Update Order Status'),
		fields: [
			{
				fieldtype: 'Select',
				fieldname: 'status',
				label: __('New Status'),
				options: 'Draft\nSubmitted\nPreparing\nReady\nServed\nPaid\nCancelled',
				reqd: 1,
				default: frm.doc.status
			}
		],
		primary_action: function() {
			let values = dialog.get_values();
			if (values.status) {
				update_order_status(frm, values.status);
				dialog.hide();
			}
		},
		primary_action_label: __('Update')
	});
	dialog.show();
}

function show_payment_dialog(frm) {
	let dialog = new frappe.ui.Dialog({
		title: __('Add Payment'),
		fields: [
			{
				fieldtype: 'Currency',
				fieldname: 'amount',
				label: __('Payment Amount'),
				reqd: 1,
				default: frm.doc.outstanding_amount
			},
			{
				fieldtype: 'Select',
				fieldname: 'payment_method',
				label: __('Payment Method'),
				options: 'Cash\nCard\nUPI\nWallet',
				reqd: 1
			}
		],
		primary_action: function() {
			let values = dialog.get_values();
			if (values.amount && values.payment_method) {
				add_payment(frm, values.amount, values.payment_method);
				dialog.hide();
			}
		},
		primary_action_label: __('Add Payment')
	});
	dialog.show();
}

function update_order_status(frm, status) {
	frappe.call({
		method: 'update_status',
		doc: frm.doc,
		args: {
			new_status: status
		},
		callback: function(r) {
			if (r.message) {
				frm.reload_doc();
				frappe.show_alert({
					message: __('Order status updated to {0}', [status]),
					indicator: 'green'
				});
			}
		}
	});
}

function add_payment(frm, amount, payment_method) {
	frappe.call({
		method: 'add_payment',
		doc: frm.doc,
		args: {
			amount: amount,
			payment_method: payment_method
		},
		callback: function(r) {
			if (r.message) {
				frm.reload_doc();
				frappe.show_alert({
					message: __('Payment of {0} added successfully', [format_currency(amount)]),
					indicator: 'green'
				});
			}
		}
	});
}