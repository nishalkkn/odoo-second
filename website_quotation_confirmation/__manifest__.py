{
    'name': "Website Quotation Confirmation",
    'application': True,
    'version': '17.0.1.0.1',
    'summary': 'Website Quotation Confirmation',
    'description': """
This module add feature to allow customer to confirm quotation from the portal.
    """,

    'depends': [
        'base',
        'sale',
    ],

    'data': [
        'views/sale_portal_templates.xml',
    ],

    'license': 'LGPL-3',

}
