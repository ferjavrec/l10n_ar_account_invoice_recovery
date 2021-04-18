{
    'name': 'Recovery Invoice Electronic',
    'version': '11.0.0.0.0',
    'category': 'Accounting',
    'website': 'www.geneos.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'account',
    ],
    'data': [
        'view/msg_box.xml',
        'wizards/invoice_recovery_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}
