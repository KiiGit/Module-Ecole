# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from functions import *
from odoo.exceptions import ValidationError


class ResPartnerSchool(models.Model):

    _name = 'ecole.partner.school'
    _order = 'id desc'

    # Fonction qui permet de récupérer la période par défaut
    @api.multi
    def _get_period_year(self):
        domain = [('period_school_year', '=', False), ('default_school_year', '=', True)]
        period_id = self.env['ecole.partner.school.years'].search(domain, limit=1).id
        if period_id:
            return period_id

    # region Private attributes

    partner_id = fields.Many2one(string="Child", comodel_name="res.partner")

    school_year_id = fields.Many2one(string='Period',
                                     ondelete='SET NULL',
                                     comodel_name="ecole.partner.school.years",
                                     default=_get_period_year)
    school_year_id_rel = fields.Char(string='Period', store=False, compute='_compute_period_id')
    school_registration = fields.Date(string='Begin',
                                      copy=False)
    school_end_date = fields.Date(string='End',
                                  copy=False)
    default_school_year = fields.Boolean(string='Current year',
                                         readonly="1",
                                         related='school_year_id.default_school_year',
                                         copy=False)  # Pour filtre
    period_school_year = fields.Boolean(string='Next year',
                                        readonly="1",
                                        related='school_year_id.period_school_year',
                                        copy=False)  # Pour filtre
    school_name_id = fields.Many2one(comodel_name="horanet.school.establishment", string="Establishment")
    school_level_id = fields.Many2one(comodel_name="horanet.school.grade", string="Level")
    school_lvl = fields.Many2one(comodel_name="horanet.school.grade", string="Level")

    half_pension = fields.Boolean(string='Catering', copy=False)
    half_pension_previous = fields.Boolean(string='previously registered', copy=False, store=True,
                                           compute='_retrieve_halfpension_previous')
    half_pension_occasional = fields.Boolean(string='Occasional registred', copy=False)
    half_pension_begin_date = fields.Date(string='Start', copy=False)
    half_pension_end_date = fields.Date(string='End', copy=False)
    half_pension_id = fields.Many2one(comodel_name="ecole.halfpension.school", string="Place")
    half_pension_days_value = fields.Integer(string='Days value', copy=False, store=True)
    # half_pension_binary_value = fields.Char(string='Binary value', copy=False, store=False)
    half_pension_monday = fields.Boolean(string='Monday', copy=False, store=False,
                                         compute='convert_dec_bin_halfpension', readonly=False)
    half_pension_tuesday = fields.Boolean(string='Tuesday', copy=False, store=False,
                                          compute='convert_dec_bin_halfpension', readonly=False)
    half_pension_wednesday = fields.Boolean(string='Wednesday', copy=True, readonly="1", store=False,
                                            compute='convert_dec_bin_halfpension')
    half_pension_thursday = fields.Boolean(string='Thursday', copy=True, store=False,
                                           compute='convert_dec_bin_halfpension', readonly=False)
    half_pension_friday = fields.Boolean(string='Friday', copy=True, store=False,
                                         compute='convert_dec_bin_halfpension', readonly=False)
    half_pension_specification = fields.Boolean(string='Specifications', copy=False, store=False,
                                                compute='_retrieve_specification_for_view',
                                                groups="ecole.group_ecole_restauration_scolaire")
    half_pension_allergy = fields.Boolean(string='Allergies', copy=False)
    half_pension_text = fields.Text(string="Observations", copy=False,
                                    groups="ecole.group_ecole_restauration_scolaire")
    half_pension_without_pork = fields.Boolean(string='Without pork', copy=False,
                                               groups="ecole.group_ecole_restauration_scolaire")
    half_pension_without_meat = fields.Boolean(string='Without meat', copy=False,
                                               groups="ecole.group_ecole_restauration_scolaire")
    half_pension_without_bulletin = fields.Boolean(string='Without registration form', copy=False,
                                                   groups="ecole.group_ecole_restauration_scolaire")

    nursery = fields.Boolean(string='Nursery', copy=False, store=False, compute='_retrieve_nursery_for_tab')
    nursery_morning = fields.Boolean(string='Nursery morning', copy=False)
    nursery_evening = fields.Boolean(string='Nursery evening', copy=False)
    nursery_begin_date = fields.Date(string='Start', copy=False)
    nursery_end_date = fields.Date(string='End', copy=False)
    nursery_name_id = fields.Many2one(comodel_name="ecole.nursery.school", string="Place")
    nursery_morning_days_value = fields.Integer(string='Days value', copy=False, store=True)
    nursery_monday_morning = fields.Boolean(string='Monday morning', copy=False, store=False,
                                            compute='convert_for_nursery_morning', readonly=False)
    nursery_tuesday_morning = fields.Boolean(string='Tuesday morning', copy=False, store=False,
                                             compute='convert_for_nursery_morning', readonly=False)
    nursery_wednesday_morning = fields.Boolean(string='Wednesday morning', copy=False, store=False,
                                               compute='convert_for_nursery_morning', readonly=False)
    nursery_thursday_morning = fields.Boolean(string='Thursday morning', copy=False, store=False,
                                              compute='convert_for_nursery_morning', readonly=False)
    nursery_friday_morning = fields.Boolean(string='Friday morning', copy=False, store=False,
                                            compute='convert_for_nursery_morning', readonly=False)
    nursery_evening_days_value = fields.Integer(string='Days value', copy=False, store=True)
    nursery_monday_evening = fields.Boolean(string='Monday evening', copy=False, store=False,
                                            compute='convert_for_nursery_evening', readonly=False)
    nursery_tuesday_evening = fields.Boolean(string='Tuesday evening', copy=False, store=False,
                                             compute='convert_for_nursery_evening', readonly=False)
    nursery_wednesday_evening = fields.Boolean(string='Wednesday evening', copy=False, store=False,
                                               compute='convert_for_nursery_evening', readonly=False)
    nursery_thursday_evening = fields.Boolean(string='Thursday evening', copy=False, store=False,
                                              compute='convert_for_nursery_evening', readonly=False)
    nursery_friday_evening = fields.Boolean(string='Friday evening', copy=False, store=False,
                                            compute='convert_for_nursery_evening', readonly=False)
    nursery_text = fields.Text(string="Observations", groups="ecole.group_ecole_garderie")

    resp_civility1 = fields.Char(string="Civility", copy=False)
    resp_name1 = fields.Char(string="Name and First name", copy=False)
    resp_cp1 = fields.Char(string="Postal code", copy=False)
    resp_address1 = fields.Char(string="Address", copy=False)
    resp_town1 = fields.Char(string="Town", copy=False)
    resp_phone1 = fields.Char(string="Phone", copy=False)
    resp_filiation1 = fields.Char(string="Filiation", copy=False)
    resp_civility2 = fields.Char(string="Civility", copy=False)
    resp_name2 = fields.Char(string="Name and First name", copy=False)
    resp_cp2 = fields.Char(string="Postal code", copy=False)
    resp_address2 = fields.Char(string="Address", copy=False)
    resp_town2 = fields.Char(string="Town", copy=False)
    resp_phone2 = fields.Char(string="Phone", copy=False)
    resp_filiation2 = fields.Char(string="Filiation", copy=False)
    responsible_partner = fields.Many2one(string="Responsible",
                                          comodel_name="res.partner",
                                          ondelete='restrict',
                                          domain="[('company_type','=','person')]",
                                          delegate=False)
    status_ws = fields.Char(string="Statut", copy=False, store=True)

    # endregion

# Fonction qui permet de décocher les jours d'inscription si le booléen "inscription occasionel" est coché
    @api.onchange('half_pension_occasional')
    def _days_registration_halfpension(self):
        if self.half_pension_occasional:
            self.half_pension_monday = False
            self.half_pension_tuesday = False
            self.half_pension_thursday = False
            self.half_pension_friday = False
        else:
            self.half_pension_monday = True
            self.half_pension_tuesday = True
            self.half_pension_thursday = True
            self.half_pension_friday = True

# Récupère le titulaire respondable d'un partner
    @api.multi
    @api.onchange('partner_id')
    def _get_active_foyer(self):
        print ('test', self._origin.id)
        partner_id = self.partner_id.id
        print partner_id
        print self.env['res.partner'].browse(self.env.context.get('active_id')).id
        for record in self:
            if record.partner_id:
                # partner_id = self.partner_id.id
                # print partner_id
                print ('test', self._origin.id)
                records_foyer_id = self.env['horanet.relation.foyer'].search([('partner_id', '=', 145536)])
                print records_foyer_id
                for rec_foyer in records_foyer_id:
                    if rec_foyer.foyer_id:
                        records_partner_id = self.env['horanet.relation.foyer'].search(
                            [('foyer_id', '=', rec_foyer.foyer_id.id)])
                        for rec_partner in records_partner_id:
                            if rec_partner.partner_id:
                                self.responsible_partner = rec_partner.partner_id.id
                                print self.responsible_partner.name

# Récupère la valeur des champs booléens garderie matin ou soir pour la visualiser dans l'onglet scolaire
    @api.depends('nursery_morning', 'nursery_evening')
    def _retrieve_nursery_for_tab(self):
        for rec in self:
            if rec.nursery_morning or rec.nursery_evening:
                rec.nursery = True

# Récupère la valeur des champs booléens pour simplifier la vue liste des élèves - restauration scolaire
    @api.depends('half_pension_allergy',
                 'half_pension_without_pork',
                 'half_pension_without_meat',
                 'half_pension_allergy')
    def _retrieve_specification_for_view(self):
        for rec in self:
            if rec.half_pension_allergy or rec.half_pension_without_pork or rec.half_pension_without_meat \
                    or rec.half_pension_allergy:
                rec.half_pension_specification = True

# Récupère la valeur du champs booléen inscription de l'année précédente
    @api.depends('half_pension')
    def _retrieve_halfpension_previous(self):
        for record in self:
            res_halfpension = self.env['ecole.partner.school'].search([('id', '<', record.id),
                                                                       ('partner_id', '=', record.partner_id.id)],
                                                                      limit=1, order='id desc')
            if res_halfpension:
                record.half_pension_previous = res_halfpension.half_pension

# Récupère le niveau scolaire en fonction de l'établissement
# Récupère le lieu de restauration en fonction de l'établissement
# Récupère le lieu de garderie en fonction de l'établissement
    @api.onchange('school_name_id')
    def _retrieve_grade_id(self):
        if self.school_name_id:
            # Récupère le dernier élément du name (horanet.school.establishment)
            establishment = self.school_name_id.name.split()[-1]
            records = self.env['horanet.school.grade'].search([])
            records_halfpension = self.env['ecole.halfpension.school'].search([])
            records_nursery = self.env['ecole.nursery.school'].search([])
            for rec in records:
                if rec.name:
                    level = rec.name
                    # Si ce que contient la variable establishment est dans la variable level
                    if establishment in level:
                        # Alors le champ school_level_id sera égale au premier champ dont la valeur trouvé est identique
                        self.school_level_id = rec.id
                        self.school_lvl = rec.id
                        break
            for record in records_halfpension:
                if record.name:
                    place_halfpension = record.name.split()[-1]
                    if place_halfpension in self.school_name_id.name:
                        self.half_pension_id = record.id
                        break
            for record in records_nursery:
                if record.name:
                    place_nursery = record.name.split()[-1]
                    if place_nursery in self.school_name_id.name:
                        self.nursery_name_id = record.id
                        break

# Fonction qui permet d'éviter des chevauchement de dates (inscriptions scolaires).
    @api.multi
    def no_duplicate_school_dates(self):
        for record in self:
            if record.school_registration or record.school_end_date:
                if record.school_registration > record.school_end_date:
                    raise ValidationError("Erreur : Problème dates. Merci de modifier")
                # Récupère les enregistrement actifs sauf l'actuel
                records = self.env['ecole.partner.school'].search([('id', '<', record.id),
                                                                   ('partner_id', '=', record.partner_id.id)])
                for rec in records:
                    if rec.school_year_id == record.school_year_id:
                        if rec.school_registration and rec.school_end_date:
                            if rec.school_name_id == self.school_name_id and rec.school_level_id == self.school_level_id:
                                if (rec.school_registration <= self.school_registration <= rec.school_end_date)\
                                        or (rec.school_registration <= self.school_end_date <= rec.school_end_date):
                                    raise ValidationError("Erreur : La plage de date en chevauche une autre. "
                                                          "Merci de modifier l'enregistrement précédent")
                            else:
                                end_date = self.school_registration
                                rec.school_end_date = fields.Date.from_string(end_date) + datetime.timedelta(-1)
                                break

# Fonction qui permet d'éviter des modifications de période sur un même enregistrement.
#     @api.multi
#     def no_duplicate_period(self):
#         if self.school_year_id:
#             for rec in self:
#                 if rec.school_year_id != self.school_year_id:
#                     raise ValidationError("Erreur : Veuillez créer un autre enregistrement si vous "
#                                           "changer de période scolaire")


# Fonction qui permet d'avoir une plage de dates compris dans la période scolaire
#   @api.constrains('school_year_id')
    @api.onchange('school_registration', 'school_end_date')
    def date_included_period(self):
        if self.school_year_id:
            begin_period_years = fields.Date.from_string(self.school_year_id.year_begin_date)
            end_period_years = fields.Date.from_string(self.school_year_id.year_end_date)
            begin_period = fields.Date.from_string(self.school_registration)
            end_period = fields.Date.from_string(self.school_end_date)
            begin_halfpension = fields.Date.from_string(self.half_pension_begin_date)
            end_halfpension = fields.Date.from_string(self.half_pension_end_date)
            begin_nursery = fields.Date.from_string(self.nursery_begin_date)
            end_nursery = fields.Date.from_string(self.nursery_end_date)
            if begin_period < begin_period_years or end_period > end_period_years:
                raise ValidationError("Erreur : Veuillez respecter la période scolaire qui doit être comprise "
                                      "entre le " + str(begin_period_years.strftime('%d-%m-%Y')) + " et "
                                      "le " + str(end_period_years.strftime('%d-%m-%Y')))
            if begin_halfpension < begin_period_years or end_halfpension > end_period_years:
                raise ValidationError("Erreur : Veuillez respecter la période scolaire qui doit être comprise "
                                      "entre le " + str(begin_period_years.strftime('%d-%m-%Y')) + " et "
                                      "le " + str(end_period_years.strftime('%d-%m-%Y')) + " - Restauration")
            if begin_nursery < begin_period_years or end_nursery > end_period_years:
                raise ValidationError("Erreur : Veuillez respecter la période scolaire qui doit être comprise "
                                      "entre le " + str(begin_period_years.strftime('%d-%m-%Y')) + " et "
                                      "le " + str(end_period_years.strftime('%d-%m-%Y')) + " - Garderie")


# Fonction qui permet d'avoir un visuel sur la période actuelle sur la fiche principale
    @api.depends('school_year_id')
    def _compute_period_id(self):
        for record in self:
            if record.school_year_id:
                record.school_year_id_rel = record.school_year_id.school_years


# Fonction relation entre début d'année scolaire et début des différentes parties
    @api.onchange('school_year_id')
    def _change_begin_date(self):
        if self.school_year_id:
            begin_date_id = self.school_year_id.year_begin_date
            begin_date = fields.Date.from_string(begin_date_id)
            date_j = datetime.date.today()
            if begin_date > date_j:
                self.school_registration = begin_date_id
                self.half_pension_begin_date = begin_date_id
                self.nursery_begin_date = begin_date_id
            else:
                self.school_registration = date_j
                self.half_pension_begin_date = date_j
                self.nursery_begin_date = date_j

# Fonction relation entre fin d'année scolaire et fin des différentes parties
    @api.onchange('school_year_id')
    def _change_end_date(self):
        if self.school_year_id:
            end_date_id = self.school_year_id.year_end_date
            self.school_end_date = end_date_id
            self.half_pension_end_date = end_date_id
            self.nursery_end_date = end_date_id

# Fonction qui modifie la valeur du booleen selon l'état du champ half_pension
    @api.onchange('half_pension')
    def _default_day_halfpension_value(self):
        if self.half_pension:
            self.half_pension_monday = self.half_pension
            self.half_pension_tuesday = self.half_pension
            self.half_pension_thursday = self.half_pension
            self.half_pension_friday = self.half_pension
        else:
            self.half_pension_monday = False
            self.half_pension_tuesday = False
            self.half_pension_thursday = False
            self.half_pension_friday = False

# Fonction qui modifie la valeur du booleen selon l'état du champ nursery_morning
    @api.onchange('nursery_morning')
    def default_day_nursery_morning_value(self):
        if self.nursery_morning:
            self.nursery_monday_morning = self.nursery_morning
            self.nursery_tuesday_morning = self.nursery_morning
            self.nursery_wednesday_morning = self.nursery_morning
            self.nursery_thursday_morning = self.nursery_morning
            self.nursery_friday_morning = self.nursery_morning
        else:
            self.nursery_monday_morning = False
            self.nursery_tuesday_morning = False
            self.nursery_wednesday_morning = False
            self.nursery_thursday_morning = False
            self.nursery_friday_morning = False

# Fonction qui modifie la valeur du booleen selon l'état du champ nursery_evening
    @api.onchange('nursery_evening')
    def default_day_nursery_evening_value(self):
        if self.nursery_evening:
            self.nursery_monday_evening = self.nursery_evening
            self.nursery_tuesday_evening = self.nursery_evening
            self.nursery_wednesday_evening = self.nursery_evening
            self.nursery_thursday_evening = self.nursery_evening
            self.nursery_friday_evening = self.nursery_evening
        else:
            self.nursery_monday_evening = False
            self.nursery_tuesday_evening = False
            self.nursery_wednesday_evening = False
            self.nursery_thursday_evening = False
            self.nursery_friday_evening = False

# Fonction qui converti en binaire qui permet de synchroniser une valeur
# en binaire et les jours de la semaine - Garderie matin
    @api.onchange('nursery_morning', 'nursery_monday_morning', 'nursery_tuesday_morning', 'nursery_wednesday_morning',
                  'nursery_thursday_morning', 'nursery_friday_morning')
    def convert_bin_dec_nursery_morning(self):
        for record in self:
            if record.nursery_morning:
                # Appel de la fonction qui permet de calculé une valeur décimal selon les jours de semaines
                total_decimal = calcul_decimal_value(record.nursery_monday_morning, record.nursery_tuesday_morning,
                                                     record.nursery_wednesday_morning, record.nursery_thursday_morning,
                                                     record.nursery_friday_morning)
                # On stocke la valeur retourné dans le champs qui stocke la valeur décimale
                record.nursery_morning_days_value = total_decimal
                # On met le statut de l'inscription a 2 pour l'inscription restauration scolaire
                # record.status_ws = "2"
            else:
                record.nursery_morning_days_value = 0
                # record.status_ws = "3"

# Fonction qui converti en binaire qui permet de synchroniser une valeur
# en binaire et les jours de la semaine - Garderie soir
    @api.onchange('nursery_evening', 'nursery_monday_evening', 'nursery_tuesday_evening', 'nursery_wednesday_evening',
                  'nursery_thursday_evening', 'nursery_friday_evening')
    def convert_bin_dec_nursery_evening(self):
        for record in self:
            if record.nursery_evening:
                # Appel de la fonction qui permet de calculé une valeur décimal selon les jours de semaines
                total_decimal = calcul_decimal_value(record.nursery_monday_evening, record.nursery_tuesday_evening,
                                                     record.nursery_wednesday_evening, record.nursery_thursday_evening,
                                                     record.nursery_friday_evening)
                # On stocke la valeur retourné dans le champs qui stocke la valeur décimale
                record.nursery_evening_days_value = total_decimal
                # On met le statut de l'inscription a 2 pour l'inscription restauration scolaire
                # record.status_ws = "2"
            else:
                record.nursery_evening_days_value = 0
                # record.status_ws = "3"

# Fonction qui converti en binaire qui permet de synchroniser une valeur
# en binaire et les jours de la semaine - Restauration
    @api.onchange('half_pension', 'half_pension_monday', 'half_pension_tuesday', 'half_pension_wednesday',
                  'half_pension_thursday', 'half_pension_friday')
    def convert_bin_dec_halfpension(self):
        for record in self:
            if record.half_pension:

                # Appel de la fonction qui permet de calculé une valeur décimal selon les jours de semaines
                total_decimal = calcul_decimal_value(record.half_pension_monday, record.half_pension_tuesday,
                                                     record.half_pension_wednesday, record.half_pension_thursday,
                                                     record.half_pension_friday)
                # On stocke la valeur retourné dans le champs qui stocke la valeur décimale
                record.half_pension_days_value = total_decimal
                # On met le statut de l'inscription a 2 pour l'inscription restauration scolaire
                record.status_ws = "2"
            else:
                record.half_pension_days_value = 0
                record.status_ws = "3"

# Fonction qui permet d'avoir un visuel sur les jours d'inscription - Garderie matin
    @api.depends('nursery_morning_days_value')
    def convert_for_nursery_morning(self):
        for rec in self:
            if rec.nursery_morning_days_value:
                # converti un nombre décimal en valeur binaire
                values = dec2bin(rec.nursery_morning_days_value, 7)
                # rec.half_pension_binary_value = values

                # on crée une liste de valeur binaire
                list_values = []
                for lettre in values:
                    list_values.append(lettre)

                # On parcours les éléments de la liste
                # On sépare dans des variables nos valeurs qu'on converti en True ou False si la valeur est 1 ou 0
                if list_values[6] != '0':
                    rec.nursery_monday_morning = True
                else:
                    rec.nursery_monday_morning = False
                if list_values[5] != '0':
                    rec.nursery_tuesday_morning = True
                else:
                    rec.nursery_tuesday_morning = False
                if list_values[4] != '0':
                    rec.nursery_wednesday_morning = True
                else:
                    rec.nursery_wednesday_morning = False
                if list_values[3] != '0':
                    rec.nursery_thursday_morning = True
                else:
                    rec.nursery_thursday_morning = False
                if list_values[2] != '0':
                    rec.nursery_friday_morning = True
                else:
                    rec.nursery_friday_morning = False

# Fonction qui permet d'avoir un visuel sur les jours d'inscription - Garderie soir
    @api.depends('nursery_evening_days_value')
    def convert_for_nursery_evening(self):
        for rec in self:
            if rec.nursery_evening_days_value:
                # converti un nombre décimal en valeur binaire
                values = dec2bin(rec.nursery_evening_days_value, 7)
                # rec.half_pension_binary_value = values

                # on crée une liste de valeur binaire
                list_values = []
                for lettre in values:
                    list_values.append(lettre)

                # On parcours les éléments de la liste
                # On sépare dans des variables nos valeurs qu'on converti en True ou False si la valeur est 1 ou 0
                if list_values[6] != '0':
                    rec.nursery_monday_evening = True
                else:
                    rec.nursery_monday_evening = False
                if list_values[5] != '0':
                    rec.nursery_tuesday_evening = True
                else:
                    rec.nursery_tuesday_evening = False
                if list_values[4] != '0':
                    rec.nursery_wednesday_evening = True
                else:
                    rec.nursery_wednesday_evening = False
                if list_values[3] != '0':
                    rec.nursery_thursday_evening = True
                else:
                    rec.nursery_thursday_evening = False
                if list_values[2] != '0':
                    rec.nursery_friday_evening = True
                else:
                    rec.nursery_friday_evening = False

# Fonction qui permet d'avoir un visuel sur les jours d'inscription à la restauration scolaire
    @api.depends('half_pension_days_value')
    def convert_dec_bin_halfpension(self):
        for rec in self:
            if rec.half_pension_days_value:
                # converti un nombre décimal en valeur binaire
                values = dec2bin(rec.half_pension_days_value, 7)
                # rec.half_pension_binary_value = values

                # on crée une liste de valeur binaire
                list_values = []
                for lettre in values:
                    list_values.append(lettre)

                # On parcours les éléments de la liste
                # On sépare dans des variables nos valeurs qu'on converti en True ou False si la valeur est 1 ou 0
                if list_values[6] != '0':
                    rec.half_pension_monday = True
                else:
                    rec.half_pension_monday = False
                if list_values[5] != '0':
                    rec.half_pension_tuesday = True
                else:
                    rec.half_pension_tuesday = False
                if list_values[4] != '0':
                    rec.half_pension_wednesday = True
                else:
                    rec.half_pension_wednesday = False
                if list_values[3] != '0':
                    rec.half_pension_thursday = True
                else:
                    rec.half_pension_thursday = False
                if list_values[2] != '0':
                    rec.half_pension_friday = True
                else:
                    rec.half_pension_friday = False

# Fonction qui permet de synchroniser cantine et établissement scolaire avec SmartBambi
    @api.multi
    def changed_half_pension(self):
        for record in self:
            if record.half_pension:
                print "Inscription en cours"
                self.create_compte_cantine()
            else:
                print "Désinscription en cours"
                # self.create_compte_cantine()

    @api.multi
    def create_compte_cantine(self):
        print "En cours de traitement avec SmartBase..."

        # Garanti qu'un seul enregistrement est transmis (singleton sinon erreur)
        # self.ensure_one()
        # halfpension = self.env['ecole.halfpension.update'].search([], limit=1).mapped('halfpension')
        if self.half_pension_id:
            # Récupère les identifiants de l'usager et du titulaire
            idUsager = self.partner_id.importid_SmartBambi

            # Pour idTitu, conversion de importid_Foyer_SmartBambi pour récupérer la chaîne entre crochet
            idTituFoyer = self.partner_id.importid_Foyer_SmartBambi
            idTitu = idTituFoyer.split()[1].strip('[]')

            if idTitu and idUsager:
                from suds.client import Client
                import os
                folder = os.path.join(os.path.dirname(__file__), os.pardir)
                file_cfg = "file://" + os.path.abspath(folder + "/static/src/wsdl/smartIntegral.wsdl")
                c = Client(file_cfg)
                monstringxml = self.get_data_xml_cantine(idTitu, idUsager)
                resp = c.service.XmlAjouterUnEvenement(Synchrone=1, donneesXml=monstringxml)
                print "communication pour : " + idTitu + " réussie"

    def get_data_xml_cantine(self, idTitu, idUsager):
        from datetime import date, datetime, timedelta

        # Récupère les différentes dates
        datedeb = datetime.strftime((datetime.now()).date(), '%m/%d/%Y %H:%M:%S')
        debinscr = self.half_pension_begin_date # a convertir en datetime %m/%d/%Y %H:%M:%S
        finComptes = (datetime.now() + timedelta(days=7300)).date()
        datefinComptes = datetime.strftime(finComptes, '%m/%d/%Y %H:%M:%S')
        datefin = self.half_pension_end_date

        # Récupère le statut
        status = self.status_ws

        # Récupère la valeur binaire es jours de la semaine et mise en place dans une liste
        values = self.half_pension_binary_value
        list_values = []
        for lettre in values:
            list_values.append(lettre)
        # print "Liste valeurs->", list_values
        # print "Statut", status

        # # On sépare dans des variables nos valeurs
        monday = list_values[6]
        tuesday = list_values[5]
        wednesday = list_values[4]
        thursday = list_values[3]
        friday = list_values[2]
        saturday = list_values[1]
        sunday = list_values[0]

        # Récupère les codes et le libellé par rapport à l'établissement de restauration scolaire choisi
        code_produit = self.half_pension_id.code_Product
        code_CDG = self.half_pension_id.code_CDG
        code_Catalog = self.half_pension_id.code_Catalog
        libelle = self.half_pension_id.name

        idEtablissement = self.school_name_id.id_establishment
        idClasse = self.school_level_id.id_class

        xml ="""<CVQImportExport xmlns="www.horanet.com">
                   <Version>2</Version>
                   <CodeFournisseur>9792000100</CodeFournisseur>
                   <CodeApplication>1</CodeApplication>
                   <CodeTeleProcedure>0</CodeTeleProcedure>
                   <Comptes>
                      <Compte>
                         <CodeCentreGestion>"""+code_CDG+"""</CodeCentreGestion>
                         <Statut>1</Statut>
                         <IdCompte></IdCompte>
                         <IdTitulaire>"""+idTitu+"""</IdTitulaire>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebutContrat>"""+datedeb+"""</DateDebutContrat>
                         <Libelle>Compte Loisirs """+libelle+"""</Libelle>
                         <DateFinContrat>"""+datefinComptes+"""</DateFinContrat>
                         <TypeCompte>2</TypeCompte>
                         <CodeCatalogue>"""+code_Catalog+"""</CodeCatalogue>
                         <Tarifs>
                            <Tarif>
                               <CodeTarif/>
                               <CodePeriodeTarifaire/>
                               <CodeDevise/>
                               <CodeProduit/>
                               <MontantTarif/>
                            </Tarif>
                         </Tarifs>
                      </Compte>
                   </Comptes>
                   <Inscriptions>
                      <Inscription>
                         <IdCVQ/>
                         <Type>0</Type>
                         <Statut>"""+status+"""</Statut>
                         <DateDemande>"""+datedeb+"""</DateDemande>
                         <DateDebut>"""+debinscr+"""</DateDebut>
                         <DateFin>"""+datefin+"""</DateFin>
                         <ProfilHebdo>
                            <Lundi>"""+monday+"""</Lundi>
                            <Mardi>"""+tuesday+"""</Mardi>
                            <Mercredi>"""+wednesday+"""</Mercredi>
                            <Jeudi>"""+thursday+"""</Jeudi>
                            <Vendredi>"""+friday+"""</Vendredi>
                            <Samedi>"""+saturday+"""</Samedi>
                            <Dimanche>"""+sunday+"""</Dimanche>
                         </ProfilHebdo>
                         <Id>"""+idUsager+"""</Id>
                         <CodeCentreGestionProduit>"""+code_CDG+"""</CodeCentreGestionProduit>
                         <CodeCatalogueProduit>"""+code_Catalog+"""</CodeCatalogueProduit>
                         <ReferenceProduitCVQ>"""+code_produit+"""</ReferenceProduitCVQ>
                         <ReferenceProduit>"""+code_produit+"""</ReferenceProduit>
                         <NombrePassage />
                         <PrioritesPassage>
                            <Lundi>"""+monday+"""</Lundi>
                            <Mardi>"""+tuesday+"""</Mardi>
                            <Mercredi>"""+wednesday+"""</Mercredi>
                            <Jeudi>"""+thursday+"""</Jeudi>
                            <Vendredi>"""+friday+"""</Vendredi>
                            <Samedi>"""+saturday+"""</Samedi>
                            <Dimanche>"""+sunday+"""</Dimanche>
                         </PrioritesPassage>
                         <NumeroCompte>0</NumeroCompte>
                         <TypeCompte>2</TypeCompte>
                         <IdTitulaire>"""+idTitu+"""</IdTitulaire>
                         <CodeTarif/>
                      </Inscription>
                   </Inscriptions>
                   <UsagersClasseEtablissementScolaire>
                      <Usager>
                         <IdUsager>"""+idUsager+"""</IdUsager>
                         <IdClasse>"""+idClasse+"""</IdClasse>
                         <IdEtablissement>"""+idEtablissement+"""</IdEtablissement>  
                      </Usager>
                   </UsagersClasseEtablissementScolaire>
                </CVQImportExport>"""
        return xml

# Appel cette méthode quand on créé un nouvel enregistrement (inscription cantine)
    @api.model
    def create(self, vals):
        record = super(ResPartnerSchool, self).create(vals)
        record.no_duplicate_school_dates()
        # record.changed_half_pension()
        return record

# Appel cette méthode quand on modifie un enregistrement (inscription cantine)
    @api.multi
    def write(self, vals):
        result = super(ResPartnerSchool, self).write(vals)
        self.no_duplicate_school_dates()
        # self.no_duplicate_period()
        # self.changed_half_pension()
        return result
