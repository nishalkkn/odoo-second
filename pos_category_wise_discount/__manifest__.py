{
    'name': 'POS Category wise discount',
    'application': True,
    'version': '17.0.1.0.1',
    'summary': 'POS Category wise discount',
    'description': """

    """,

    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/res_config_settings.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_category_wise_discount/static/src/pos_discount.js',
        ],
    },

    'license': 'LGPL-3'

}
