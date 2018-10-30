# -*- coding: utf-8 -*-
{
    'name': "Ecole",
    'version': '0.1',
    'summary': """
        Module de Parthenay-Gâtine pour la base de ses développements autour du service scolaire""",

    'description': """
        Module Parthenay-Gâtine comprenant les différentes définitions pour les devs Parthenay.
      
    """,
    'installable': True,
    'auto_install': False,

    'author': "Communauté de communes de Parthenay-Gâtine",
    'website': "http://www.cc-parthenay-gatine.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Parthenay',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'horanet_school', 'horanet_tpa', 'horanet_tpa_smartbambi', 'cvq'],

    'data': [
        'data/ir_module_category.xml',
        'data/default_data.xml',

        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/school.xml',

        'views/schoolyears.xml',
        'views/updatestudent.xml',
        'views/halfpension.xml',
        'views/nursery.xml',
        'views/halfpension_place.xml',
        'views/report_certificate.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
