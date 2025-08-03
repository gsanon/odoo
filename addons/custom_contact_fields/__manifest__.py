{
    'name': 'Custom Contact Fields',
    'version': '1.0',
    'summary': 'Add custom fields to contacts',
    'description': 'Custom fields for contact management',
    'author': 'Guillaume SANON',
    'website': 'https://www.goldaia.com',
    'category': 'Contacts',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}