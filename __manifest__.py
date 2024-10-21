{
    "name": "My first app",
    'version': '1.0',
    "summary": "my fisrt app",
    "description": "my first app",
    "depends": [
        "base","sale","account","mail","contacts"
    ],
    "data": [
        'security/security.xml',  #security
        'security/ir.model.access.csv',  #security
        'data/sequences.xml',  #security
        'views/base_menu.xml',           #front end
        'views/property_view.xml',       #front end
        'views/owner_view.xml',       #front end
        'views/tag_view.xml',       #front end
        'views/sale_order_view.xml',       #front end
        'views/res_partner_order_view.xml',       #front end
        'views/building_view.xml',       #front end
        'views/property_history_view.xml',       #front end
        'wizard/change_state_view.xml',       #front end
        'reports/property_report.xml',     #front end



    ],

    'assets':{
        'web.assets_backend':['my_first_app/static/src/css/property.css']
    },

    'license': 'LGPL-3',
    'application':'true',
}
