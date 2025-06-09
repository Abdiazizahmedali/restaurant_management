# Restaurant Management System for ERPNext v15

A comprehensive restaurant management module for ERPNext v15 that provides complete functionality for managing restaurant operations including orders, tables, menu items, and reporting.

## Features

### Core Functionality
- **Restaurant Tables Management**: Manage table capacity, status, and reservations
- **Order Management**: Handle dine-in, takeaway, and delivery orders
- **Menu Categories**: Organize menu items by categories
- **Real-time Status Updates**: Track order and table status in real-time
- **Payment Integration**: Handle multiple payment methods and partial payments

### Advanced Features
- **Web Form Integration**: Online ordering system for customers
- **Comprehensive Reporting**: Daily sales, table occupancy, and analytics
- **Stock Integration**: Automatic stock consumption for inventory items
- **Tax Calculations**: Integrated tax templates and calculations
- **Role-based Permissions**: Restaurant Manager and Staff roles

### Technical Features
- **ERPNext v15 Compatible**: Built specifically for ERPNext version 15
- **Modern UI/UX**: Responsive design with custom CSS and JavaScript
- **API Integration**: RESTful APIs for external integrations
- **Custom Workflows**: Automated status updates and notifications
- **Print Formats**: Professional receipts and reports

## Installation

### Prerequisites
- ERPNext v15.x
- Frappe Framework v15.x
- Python 3.8+
- Node.js 16+

### Installation Steps

1. **Download the module**
   ```bash
   cd ~/frappe-bench/apps
   git clone [your-repository-url] restaurant_management
   ```

2. **Install the app**
   ```bash
   cd ~/frappe-bench
   bench install-app restaurant_management
   ```

3. **Install on site**
   ```bash
   bench --site [your-site] install-app restaurant_management
   ```

4. **Migrate the database**
   ```bash
   bench --site [your-site] migrate
   ```

5. **Build assets**
   ```bash
   bench build
   ```

6. **Restart services**
   ```bash
   bench restart
   ```

## Configuration

### Initial Setup

1. **Create Menu Categories**
   - Go to Restaurant Management > Menu Category
   - Create categories like "Appetizers", "Main Course", "Beverages", etc.

2. **Setup Restaurant Tables**
   - Go to Restaurant Management > Restaurant Table
   - Add all your restaurant tables with capacity and location

3. **Configure Menu Items**
   - Go to Restaurant Management > Item (or use existing Item master)
   - Mark items as "Is Sales Item" and set standard rates
   - Assign items to appropriate menu categories

4. **Setup Tax Templates**
   - Configure Sales Taxes and Charges Template for your tax requirements
   - Link tax templates to orders for automatic tax calculation

### User Roles

The module comes with two predefined roles:

- **Restaurant Manager**: Full access to all features
- **Restaurant Staff**: Limited access for day-to-day operations

## Usage

### Taking Orders

1. **Create New Order**
   - Go to Restaurant Management > Restaurant Order
   - Select order type (Dine In/Take Away/Delivery)
   - Choose table (for dine-in orders)
   - Add customer details

2. **Add Items**
   - Add items from the menu with quantities
   - System automatically calculates totals and taxes
   - Add special instructions if needed

3. **Submit Order**
   - Submit the order to send to kitchen
   - Table status automatically updates to "Occupied"

### Managing Tables

1. **Table Status Management**
   - View all tables in Restaurant Management > Restaurant Table
   - Update status: Available, Occupied, Reserved, Cleaning
   - Reserve tables for future bookings

2. **Real-time Updates**
   - Table status updates automatically with order status
   - View current orders for each table
   - Quick status change buttons

### Processing Payments

1. **Add Payments**
   - Use "Add Payment" button on submitted orders
   - Support for multiple payment methods
   - Handle partial payments

2. **Payment Status**
   - Automatic status updates: Unpaid, Partially Paid, Paid
   - Outstanding amount calculations
   - Integration with ERPNext Payment Entry

### Reporting

1. **Daily Sales Report**
   - Comprehensive sales analysis
   - Filter by date, order type, status
   - Export capabilities

2. **Table Occupancy Report**
   - Real-time table status overview
   - Occupancy analytics
   - Customer information

## API Endpoints

The module provides several API endpoints for external integrations:

### Orders
- `GET /api/resource/Restaurant Order` - List orders
- `POST /api/resource/Restaurant Order` - Create order
- `PUT /api/resource/Restaurant Order/{name}` - Update order

### Tables
- `GET /api/method/restaurant_management.restaurant_management.doctype.restaurant_table.restaurant_table.get_available_tables` - Get available tables
- `POST /api/method/restaurant_management.restaurant_management.doctype.restaurant_table.restaurant_table.reserve_table` - Reserve table

### Menu Items
- `GET /api/method/restaurant_management.restaurant_management.doctype.restaurant_order.restaurant_order.get_menu_items` - Get menu items

## Customization

### Adding Custom Fields

You can extend the module by adding custom fields:

```python
# In hooks.py
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Restaurant Order-custom_field_name"
                ]
            ]
        ]
    }
]
```

### Custom Scripts

Add custom client-side scripts in the `public/js/` directory and reference them in hooks.py:

```python
# In hooks.py
doctype_js = {
    "Restaurant Order": "public/js/custom_restaurant_order.js"
}
```

## Troubleshooting

### Common Issues

1. **Module not appearing after installation**
   - Check if the app is installed: `bench --site [site] list-apps`
   - Clear cache: `bench --site [site] clear-cache`
   - Rebuild: `bench build`

2. **Permission errors**
   - Ensure proper role assignments
   - Check permission rules in Role Permission Manager

3. **Database migration issues**
   - Run: `bench --site [site] migrate`
   - Check error logs: `bench --site [site] logs`

### Support

For support and bug reports:
- Create an issue in the repository
- Contact: info@yourcompany.com

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Changelog

### Version 1.0.0
- Initial release
- Core restaurant management features
- Order and table management
- Reporting and analytics
- Web form integration
- ERPNext v15 compatibility