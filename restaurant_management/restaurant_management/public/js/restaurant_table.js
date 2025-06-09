frappe.ui.form.on('Restaurant Table', {
	refresh: function(frm) {
		// Add custom buttons based on table status
		if (frm.doc.status === 'Available') {
			frm.add_custom_button(__('Reserve Table'), function() {
				reserve_table(frm);
			});
		}
		
		if (frm.doc.status === 'Occupied') {
			frm.add_custom_button(__('Mark Available'), function() {
				set_table_available(frm);
			});
		}
		
		if (frm.doc.status === 'Reserved') {
			frm.add_custom_button(__('Mark Occupied'), function() {
				set_table_occupied(frm);
			});
			
			frm.add_custom_button(__('Cancel Reservation'), function() {
				set_table_available(frm);
			});
		}
		
		// Show current orders for this table
		if (frm.doc.name) {
			show_current_orders(frm);
		}
	}
});

function reserve_table(frm) {
	frappe.call({
		method: 'reserve_table',
		doc: frm.doc,
		callback: function(r) {
			if (r.message) {
				frm.reload_doc();
				frappe.show_alert({
					message: __('Table {0} reserved successfully', [frm.doc.table_no]),
					indicator: 'orange'
				});
			}
		}
	});
}

function set_table_occupied(frm) {
	frappe.call({
		method: 'set_occupied',
		doc: frm.doc,
		callback: function(r) {
			if (r.message) {
				frm.reload_doc();
				frappe.show_alert({
					message: __('Table {0} marked as occupied', [frm.doc.table_no]),
					indicator: 'red'
				});
			}
		}
	});
}

function set_table_available(frm) {
	frappe.call({
		method: 'set_available',
		doc: frm.doc,
		callback: function(r) {
			if (r.message) {
				frm.reload_doc();
				frappe.show_alert({
					message: __('Table {0} marked as available', [frm.doc.table_no]),
					indicator: 'green'
				});
			}
		}
	});
}

function show_current_orders(frm) {
	frappe.call({
		method: 'frappe.client.get_list',
		args: {
			doctype: 'Restaurant Order',
			filters: {
				table: frm.doc.name,
				status: ['not in', ['Paid', 'Cancelled']]
			},
			fields: ['name', 'customer_name', 'status', 'grand_total', 'order_time']
		},
		callback: function(r) {
			if (r.message && r.message.length > 0) {
				let orders_html = '<div class="table-orders"><h5>Current Orders:</h5>';
				r.message.forEach(order => {
					orders_html += `
						<div class="order-item" style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px;">
							<strong><a href="/app/restaurant-order/${order.name}">${order.name}</a></strong><br>
							Customer: ${order.customer_name}<br>
							Status: <span class="indicator ${get_status_color(order.status)}">${order.status}</span><br>
							Amount: ${format_currency(order.grand_total)}<br>
							Time: ${moment(order.order_time).format('DD-MM-YYYY HH:mm')}
						</div>
					`;
				});
				orders_html += '</div>';
				
				frm.dashboard.add_section(orders_html, __('Current Orders'));
			}
		}
	});
}

function get_status_color(status) {
	const status_colors = {
		'Draft': 'grey',
		'Submitted': 'blue',
		'Preparing': 'orange',
		'Ready': 'yellow',
		'Served': 'green',
		'Paid': 'green',
		'Cancelled': 'red'
	};
	return status_colors[status] || 'grey';
}