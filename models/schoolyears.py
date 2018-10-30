# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolYears(models.Model):

    _name = "ecole.partner.school.years"
    _rec_name = "school_years"  # POUR ASSIGNER PAR DEFAUT UN AUTRE CHAMP AUTRE QUE NAME
    _order = 'id desc'

    school_years = fields.Char(string='School year', required=True, copy=False)
    year_begin_date = fields.Date(string='Start date', required=True, copy=False)
    year_end_date = fields.Date(string='End date', required=True, copy=False)
    default_school_year = fields.Boolean(string='Current school year', copy=False)
    period_school_year = fields.Boolean(string='Registration period', copy=False)
    active = fields.Boolean(default=True)
