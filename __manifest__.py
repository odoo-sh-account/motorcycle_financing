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
    'depends': ['base', 'sale'],
    'data': [
        # Security
        'security/motorcycle_financing_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        # Views - Note: Order matters for proper menu creation
        'views/motorcycle_financing_menu.xml',
        'views/loan_application_views.xml',
        'views/loan_application_tag_views.xml',
        'views/loan_application_document_views.xml',
        'views/loan_application_document_type_views.xml',
    ],
}