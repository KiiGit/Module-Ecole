# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HalfPensionSchool(models.Model):

    _name = 'ecole.halfpension.school'

    name = fields.Char(string='Name')
    code_Product = fields.Char(string='Product Code')
    code_CDG = fields.Char(string='Management Center')
    code_Catalog = fields.Char(string='Product catalogue')
    group_id = fields.Many2one(comodel_name="res.groups", string="Group")
