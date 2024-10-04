{
    'name': 'Payment Provider: Paytrail',
    'application': True,
    'version': '17.0.1.0.1',
    'category': 'Accounting/Payment Providers',
    'description': " payment provider for online payments all over the world ",

    'depends': ['payment'],

    'data': [
        'views/payment_paytrail_template.xml',
        'views/payment_provider_views.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],

    'license': 'LGPL-3'
}
