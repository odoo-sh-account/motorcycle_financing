{
    'name': 'Motorcycle Financing 2.',
    'version': '18.0.0.0.1',
    'category': 'Kawiil/Custom Modules',
    'license': 'OPL-1',
    'summary': 'Streamlines the loan application process for dealerships. Alejandro',
    'description': 'A module to handle motorcycle loan applications, tracking, and management',
    'author': 'Odoo-sh-account',
    'website': 'https://github.com/odoo-sh-account/motorcycle_financing',
    'support': 'support@deleonlangure.com',
    'sequence': 10,
    'installable': True,
    'application': True,
    'auto_install': False,
    'depends': ['base'],
    'data': [
        # Security
        'security/motorcycle_financing_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        # Data files
        'data/loan_demo.xml',
        # Views and Actions
        'views/loan_application_views.xml',
        # Menus
        'views/motorcycle_financing_menu.xml',
    ],
    'demo': [],
}