1. Declarative Paradigm

- Modules are defined declaratively, not traditionally
- Python models contain core logic
- XML files define views, menus, and configurations

2. Module Structure

- `__init__.py`: Imports models
- `__manifest__.py`: Module metadata, dependencies, and load order
- Models: Business logic implemented through class methods
- Views: Defined in XML, describing UI and interactions

3. Module Loading

- Addons folder is a shared directory
- Modules must have a valid `__manifest__.py`
- Odoo scans addons when updating application list
- Modules appear in available apps but aren't automatically installed
- Manual installation required through web interface or command line

4. Key Characteristics

- Highly configurable through declarative definitions
- Minimal imperative code
- Framework handles much of the underlying implementation

5. Module Import and Model Registration

- Only top-level models need explicit import in init.py
- Auxiliary models within the same file don't require separate imports
- Helps prevent circular import issues
- Odoo's ORM handles model registration during module loading
6. Dependency Management

- Modules are isolated by default
- External module functionality accessed via depends in manifest
- "base" module provides core ORM and system infrastructure
- Explicit dependencies ensure required functionality is available

7. Configuration and Metadata

- XML files transformed into database records
- Key configuration tables include ir_model_data, ir_ui_view, ir_menu
- Module installation process: database schema first, then XML parsing

# ORM Model related information 

In Odoo, self is an ORM recordset that provides powerful methods and attributes:

- Record Navigation
    - self.ids: List of database IDs
    - self.ensure_one(): Ensures recordset has exactly one record
    - self.browse(): Navigate related records

- Database Operations
    - self.create(): Create new records
    - self.write(): Update records
    - self.unlink(): Delete records
    - self.search(): Find records

- Field Access
    - self.field_name: Access field values
    - self.mapped(): Extract field values
    - self.filtered(): Filter recordset
    - self.sorted(): Sort recordset

- Environment and Context
    - self.env: Access Odoo environment
    - self.env.user: Current user
    - self.env.company: Current company
    - self.with_context(): Modify record context

Methods starting with _ in Odoo have special meanings:

- Constraint Methods (like _check_down_payment):
    - Automatically called by Odoo's ORM during record creation/modification
    - Decorated with @api.constrains
    - Raise ValidationError if constraint is violated
    - Do not return values, they either pass silently or raise an exception
    - Triggered before database write operations

- Typical use cases:
    - Validate field values
    - Ensure data integrity
    - Prevent invalid record states
    - Provide custom validation logic beyond basic field constraints

Non-Underscore Methods in Odoo:

- Business Logic Methods
    - Triggered by user actions or UI buttons
    - Defined in model classes
    - Can modify record states and perform complex operations
    - Interact with related records using self.env and relational fields
    - Typically named with action_* prefix
    - Invoked through:
        - UI buttons
        - Programmatic calls
        - Workflow transitions

- Characteristics
    - Can modify multiple records
    - Use self.write() for record updates
    - Can raise UserError for business logic constraints
    - Scope determined by the model's view context
    - Cross-model interactions require relational fields
    - Can contain any arbitrary python code, for instance, API calls.

# Additional Odoo Model Insights

## Field Types and Decorators
- Common Field Types
    - Char: Text fields
    - Integer: Whole number fields
    - Float: Decimal number fields
    - Date: Date fields
    - Many2one: Relational fields linking to another model
    - One2many: Reverse relationship of Many2one
    - Many2many: Complex multi-record relationships

- Decorators
    - @api.depends: Trigger computation of fields
    - @api.constrains: Define field-level validation
    - @api.onchange: React to field value changes

## Model Inheritance
- Inheritance Modes
    - _inherit: Extend existing model
    - _inherits: Delegate inheritance
    - Allows modification and extension of core Odoo models

## Computed and Related Fields
- Computed Fields
    - Dynamically calculated based on other fields
    - Can be stored or non-stored
    - Defined with @api.depends decorator

- Related Fields
    - Directly reference fields in related models
    - Automatically update when source field changes

## Security and Access Rights
- Record Rules
    - Define domain-based access conditions
    - Control record visibility
    - Group-based permissions

- Access Control
    - Field-level security
    - User and group-based restrictions
    - Configurable through XML security rules

## Security Groups and Menu Visibility

### Problem
When deploying to Odoo.sh, some menu items were not visible even though the module was installed successfully. Specifically, these menus were missing:
- Loan Applications
- Applications
- Documents

### Root Cause
The issue was related to user permissions. While the module defines specific security groups:
- `financing_user` (Motorcycle Financing User)
- `financing_admin` (Motorcycle Financing Admin)

The user needs to be assigned to these groups to see the corresponding menu items. In local development environments, this might be automatically handled or you might be using a superuser account, but in production environments like Odoo.sh, proper group assignment is required.

### Solution
Either:
1. Assign the appropriate security group to the user:
   - Go to Settings > Users & Companies > Users
   - Edit the user
   - Under "Access Rights", find "Motorcycle Financing" category
   - Assign either "Motorcycle Financing User" or "Motorcycle Financing Admin"

2. Or for testing purposes, enable superuser mode (not recommended for production)

### Best Practices
1. Always test module installation with a non-admin user to catch permission-related issues early
2. Document required security groups for each feature
3. Consider implementing a data file that automatically assigns necessary groups to specified users during module installation

## View Mode Differences Between Odoo CE and EE

### Problem
When deploying to Odoo.sh (Enterprise Edition 18.0+e) we encountered the error:
```
Error: View types not defined tree found in act_window action 394
```
while the same code worked fine in local development (Community Edition 18.0-20250207).

### Root Cause
There's a difference in how view modes are handled between Odoo CE and EE:
- Community Edition is more lenient and accepts both `tree` and `list` view modes
- Enterprise Edition is stricter and requires `list` view mode specifically

### Solution
In action window definitions (`ir.actions.act_window`), always use `list,form` instead of `tree,form` for the `view_mode` field:

```xml
<record id="action_example" model="ir.actions.act_window">
    <field name="name">Example Action</field>
    <field name="res_model">example.model</field>
    <field name="view_mode">list,form</field>  <!-- Use list, not tree -->
</record>
```

This ensures compatibility with both Community and Enterprise editions.

### Note
While the XML view definition still uses `<tree>` tags, the action's `view_mode` must use `list`:
```xml
<!-- In view definition, still use tree -->
<record id="view_example_tree" model="ir.ui.view">
    <field name="arch" type="xml">
        <tree>  <!-- This stays as tree -->
            <field name="name"/>
        </tree>
    </field>
</record>

<!-- But in action definition, use list -->
<record id="action_example" model="ir.actions.act_window">
    <field name="view_mode">list,form</field>  <!-- This must be list -->
</record>
