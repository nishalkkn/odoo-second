{
    'name': 'Paytrail Payment Integration',
    'application': True,
    'version': '17.0.1.0.1',
    'summary': 'Paytrail Payment Integration',
    'description': """

    """,

    'depends': [
        'base',
        'onboarding',
        'portal',
    ],
    'data': [
        'views/payment_paytrail_templates.xml',
        'views/payment_provider_view.xml',

        'data/payment_method_data.xml',
    ],

    'license': 'LGPL-3'

}
