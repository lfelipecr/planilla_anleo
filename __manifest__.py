# -*- coding: utf-8
{
    "name": "Planilla",
    "version": "1.0",
    "author": "Francisco Villegas",
    "category": "hr",
    "description": "Planilla",
    "website": "",
    "license": "AGPL-3",
    "depends": [
        'base',
        'hr',
        'hr_contract',
        'om_hr_payroll',
        'barco',
     ],
    "demo": [
    ],
    "data": [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/ini.xml',
        'view/hr_payslip.xml',
        'view/planilla.xml',
        'view/boleta.xml',
        'view/transportes.xml',
    ],
    'css': [],
    'test': [],
    "installable": True,
    'application': False,
}
