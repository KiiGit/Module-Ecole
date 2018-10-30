# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NurserySchool(models.Model):

    _name = 'ecole.nursery.school'

    name = fields.Char(string='Nursery place', placeholder="Place - City", copy=False)
