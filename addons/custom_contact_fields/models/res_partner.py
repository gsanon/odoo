from odoo import models, fields, _

class PartnerActivity(models.Model):
    _name = 'partner.activity'
    _description = _('Partner Activity')
    _order = 'name'
    
    name = fields.Char(_('Activity'), required=True)
    description = fields.Text(_('Description'))
    active = fields.Boolean(_('Active'), default=True)


class PartnerPictureLink(models.Model):
    _name = 'partner.picture.link'
    _description = _('Partner Picture Link')
    _order = 'sequence, id'
    
    name = fields.Char(_('Description'), help=_('Optional description for this picture'))
    url = fields.Char(_('Picture URL'), required=True)
    sequence = fields.Integer(_('Sequence'), default=10)
    partner_id = fields.Many2one('res.partner', string=_('Partner'), ondelete='cascade')


class PartnerOrigin(models.Model):
    _name = 'partner.origin'
    _description = _('Partner Origin')
    
    name = fields.Char(_('Origin'), required=True)
    code = fields.Char(_('Code'))
    description = fields.Text(_('Description'))
    active = fields.Boolean(_('Active'), default=True)
    
    def name_get(self):
        # This controls how the options are displayed
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result
    

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    x_origin = fields.Many2many(
        'partner.origin',
        'partner_origin_rel',
        'partner_id',
        'origin_id',
        string=_('Origin')
    )
    x_book_fr_id = fields.Integer(string=_('Book.fr ID'), help=_('ID from Book.fr system'))
    x_external_id = fields.Char(string=_('External ID'), help=_('External system identifier'))
    x_model_pictures = fields.One2many('partner.picture.link', 'partner_id', string=_('Model Pictures'))
    
    # Basic partner fields
    x_activities = fields.Many2many(
        'partner.activity',
        'res_partner_activity_rel',
        'res_partner_id',
        'partner_activity_id',
        string=_('Partner Activities')
    )
    x_date_of_birth = fields.Date(string=_('Date of Birth'))
    x_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string=_('Gender'))
    x_instagram = fields.Char(string=_('Instagram'))
    
    # Model Details fields (moved from separate model)
    x_why_goldaia = fields.Text(_('Why Goldaia?'))
    x_application_date = fields.Date(_('Application Date'))
    x_artistic_universe = fields.Text(_('Artistic Universe'))
    x_accept_contact = fields.Boolean(_('Accept Contact'), default=False)
    x_accept_data_sharing = fields.Boolean(_('Accept Data Sharing'), default=False)
    x_nationality = fields.Char(_('Nationality'))
    x_height = fields.Float(_('Height (cm)'))
    x_weight = fields.Float(_('Weight (kg)'))
    x_top_size = fields.Selection([
        ('xxs', 'XXS'), ('xs', 'XS'), ('xs_s', 'XS/S'), ('s', 'S'), ('s_m', 'S/M'),
        ('m', 'M'), ('m_l', 'M/L'), ('l', 'L'), ('l_xl', 'L/XL'), ('xl', 'XL'),
        ('xl_xxl', 'XL/XXL'), ('xxl', 'XXL'), ('other', 'Other')
    ], string=_('Top Size'))
    x_low_waist = fields.Selection([
        ('xxs', 'XXS'), ('xs', 'XS'), ('xs_s', 'XS/S'), ('s', 'S'), ('s_m', 'S/M'),
        ('m', 'M'), ('m_l', 'M/L'), ('l', 'L'), ('l_xl', 'L/XL'), ('xl', 'XL'),
        ('xl_xxl', 'XL/XXL'), ('xxl', 'XXL'), ('other', 'Other')
    ], string=_('Low Waist'))
    x_shoe_size = fields.Float(_('Shoe Size'))
    x_eyes_color = fields.Selection([
        ('blue', 'Blue'), ('brown', 'Brown'), ('grey', 'Grey'), 
        ('green', 'Green'), ('hazelnut', 'Hazelnut'), ('other', 'Other')
    ], string=_('Eyes Color'))
    x_hair_color = fields.Selection([
        ('black', 'Black'), ('brown', 'Brown'), ('red', 'Red'), 
        ('blond', 'Blond'), ('white', 'White'), ('other', 'Other')
    ], string=_('Hair Color'))
    x_personal_development_interest = fields.Boolean(_('Personal Development Interest'), default=False)
    x_objectives = fields.Text(_('Objectives'))
    x_issues = fields.Text(_('Issues'))
    x_model_expectations = fields.Text(_('Model Expectations'))
    x_need_help = fields.Boolean(_('Need Help'), default=False)
    x_interested_in_support = fields.Boolean(_('Interested in Support'), default=False)

    # Image URL fields for applicant uploads
    x_applicant_image_1_url = fields.Char(_('Applicant Image 1 URL'), help=_('URL link to first uploaded image from applicant'))
    x_applicant_image_2_url = fields.Char(_('Applicant Image 2 URL'), help=_('URL link to second uploaded image from applicant'))
