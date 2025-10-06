{
    'name': 'Sale Order Partner Tag',
    'version': '1.0',
    'summary': 'Automatyczne generowanie 3-literowych tagów klientów i numeracji zamówień wg tagu.',
    'author': 'ChatGPT & User',
    'website': 'https://odoo.com',
    'category': 'Sales',
    'depends': ['sale_management'],
    'data': [
        'data/sale_order_sequence.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}