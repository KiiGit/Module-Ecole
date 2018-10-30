# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from school import *


class StudentUpdate(models.Model):
    _name = 'ecole.student.update'

# Fonction qui permet de récupérer les élèves actifs
    def _get_default_students(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_ids'))

# Fonction qui permet de récupérer l'établissement actif
    def _get_default_school(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_id')).school_name_id.id

# Fonction qui permet de récupérer la période par défaut
    @api.multi
    def _get_period_year(self):
        domain = [('period_school_year', '=', True), ('default_school_year', '=', False)]
        period_id = self.env['ecole.partner.school.years'].search(domain, limit=1).id

        return period_id

# Fonction qui permet de récupérer le niveau actif +1
    @api.multi
    def _get_default_level(self):
        level_id = self.env['ecole.partner.school'].browse(self.env.context.get('active_id'))
        new_level = level_id.school_level_id.id

        return new_level + 1

    student_ids = fields.Many2many('ecole.partner.school', String="Students", default=_get_default_students)
    school_name_id = fields.Many2one(comodel_name="horanet.school.establishment",
                                     string="Establishments",
                                     default=_get_default_school)
    school_year_id = fields.Many2one(string='Period',
                                     ondelete='SET NULL',
                                     comodel_name="ecole.partner.school.years",
                                     default=_get_period_year)
    school_level_id = fields.Many2one(comodel_name="horanet.school.grade",
                                      string="Level",
                                      default=_get_default_level)

# Fonction qui permet le passage de fin d'année scolaire
    def set_student_level(self):
        for record in self:
            if record.student_ids:
                for rec in record.student_ids:

                    # Permettra de récupérer les bonnes dates inscription scolaire et garderie
                    domain = [('period_school_year', '=', True), ('default_school_year', '=', False)]
                    records_years = self.env['ecole.partner.school.years'].search(domain, limit=1)

                    if rec.school_year_id.id+1 != self.school_year_id.id:
                        raise ValidationError("Erreur : Les périodes scolaires ne correspondent pas. Merci de corriger")

                    school_level = rec.school_level_id.name
                    if "CM2" in school_level:
                        raise ValidationError("Erreur : Vous ne pouvez pas faire de passage de fin d'année "
                                              "pour les classe de CM2")

                    # Récupère les valeurs des champs de la table ecole.partner.school
                    partner = rec.partner_id.id

                    nursery_name = rec.nursery_name_id.id
                    nursery_morning_days_value = rec.nursery_morning_days_value
                    nursery_evening_days_value = rec.nursery_evening_days_value

                    nursery_morning = rec.nursery_morning
                    nursery_evening = rec.nursery_evening

                    # Récupère les valeurs des champs de la table ecole.student.update
                    new_year = self.school_year_id.id
                    new_level = self.school_level_id.id
                    new_school = self.school_name_id.id

                    new_begin_date_id = records_years.year_begin_date
                    new_end_date_id = records_years.year_end_date

                    new_nursery_begin_date = records_years.year_begin_date
                    new_nursery_end_date = records_years.year_end_date

                    # Responsable 1 Garderie
                    resp_civility1 = rec.resp_civility1
                    resp_name1 = rec.resp_name1
                    resp_cp1 = rec.resp_cp1
                    resp_address1 = rec.resp_address1
                    resp_town1 = rec.resp_town1
                    resp_phone1 = rec.resp_phone1
                    resp_filiation1 = rec.resp_filiation1

                    # Responsable 2 Garderie
                    resp_civility2 = rec.resp_civility2
                    resp_name2 = rec.resp_name2
                    resp_cp2 = rec.resp_cp2
                    resp_address2 = rec.resp_address2
                    resp_town2 = rec.resp_town2
                    resp_phone2 = rec.resp_phone2
                    resp_filiation2 = rec.resp_filiation2

                    # Préparation du dictionnaire de valeurs
                    vals = {'partner_id': partner,
                            'school_year_id': new_year,
                            'school_registration': new_begin_date_id,
                            'school_end_date': new_end_date_id,
                            'school_name_id': new_school,
                            'school_level_id': new_level,
                            'nursery_name_id': nursery_name,
                            'nursery_begin_date': new_nursery_begin_date,
                            'nursery_end_date': new_nursery_end_date,
                            'nursery_morning': nursery_morning,
                            'nursery_evening': nursery_evening,
                            'nursery_morning_days_value': nursery_morning_days_value,
                            'nursery_evening_days_value': nursery_evening_days_value,
                            'resp_civility1': resp_civility1,
                            'resp_name1': resp_name1,
                            'resp_cp1': resp_cp1,
                            'resp_address1': resp_address1,
                            'resp_town1': resp_town1,
                            'resp_phone1': resp_phone1,
                            'resp_filiation1': resp_filiation1,
                            'resp_civility2': resp_civility2,
                            'resp_name2': resp_name2,
                            'resp_cp2': resp_cp2,
                            'resp_address2': resp_address2,
                            'resp_town2': resp_town2,
                            'resp_phone2': resp_phone2,
                            'resp_filiation2': resp_filiation2
                            }

                    record.student_ids.create(vals)

            # Retourne le popup de validation
            return {
                'name': 'Validation',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ecole.student.update',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new'
            }
