# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class Agency(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(150), nullable=False)
#     acronym = db.Column(db.String(50), nullable=True)
#     description = db.Column(db.Text, nullable=False)
#     mission_statement = db.Column(db.Text, nullable=False)
#     website = db.Column(db.String(255), nullable=False)
#     is_ngo = db.Column(db.Boolean, nullable=False)
#     years_operational = db.Column(db.Integer, nullable=False)
#     reason_for_joining = db.Column(db.Text, nullable=False)
#     willing_to_participate = db.Column(db.Boolean, nullable=False)
#     commitment_to_principles = db.Column(db.Boolean, nullable=False)

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'full_name': self.full_name,
#             'acronym': self.acronym,
#             'description': self.description,
#             'mission_statement': self.mission_statement,
#             'website': self.website,
#             'is_ngo': self.is_ngo,
#             'years_operational': self.years_operational,
#             'reason_for_joining': self.reason_for_joining,
#             'willing_to_participate': self.willing_to_participate,
#             'commitment_to_principles': self.commitment_to_principles
#         }



from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
db = SQLAlchemy()

class Agency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    acronym = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=False)
    mission_statement = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(255), nullable=False)
    is_ngo = db.Column(db.Boolean, nullable=False)
    years_operational = db.Column(db.Integer, nullable=False)
    reason_for_joining = db.Column(db.Text, nullable=False)
    willing_to_participate = db.Column(db.Boolean, nullable=False)
    commitment_to_principles = db.Column(db.Boolean, nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'acronym': self.acronym,
            'description': self.description,
            'mission_statement': self.mission_statement,
            'website': self.website,
            'is_ngo': self.is_ngo,
            'years_operational': self.years_operational,
            'reason_for_joining': self.reason_for_joining,
            'willing_to_participate': self.willing_to_participate,
            'commitment_to_principles': self.commitment_to_principles
        }
class ContactDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    clan = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, name, contact, clan, role):
        self.name = name
        self.contact = contact
        self.clan = clan
        self.role = role

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'clan': self.clan,
            'role': self.role
        }

class Consortium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active_year = db.Column(db.String(4), nullable=False)  
    partner_ngos = db.Column(db.Text, nullable=False)  
    international_staff = db.Column(db.Integer, nullable=False)
    national_staff = db.Column(db.Integer, nullable=False)
    program_plans = db.Column(db.Text, nullable=False)
    main_donors = db.Column(db.Text, nullable=False)
    annual_budget = db.Column(db.String(20), nullable=False)  
    membership_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Consortium {self.active_year}>'
    

class MemberAccountAdministrator(db.Model):

    id = db.Column(db.Integer, primary_key=True)  # Primary key for the model
    agency_registration_date = db.Column(db.Date, nullable=False)  # Date field
    agency_registration_number = db.Column(db.String(100), nullable=False)
    hq_name = db.Column(db.String(100), nullable=False)
    hq_position = db.Column(db.String(100), nullable=False)
    hq_email = db.Column(db.String(100), nullable=False)
    hq_address = db.Column(db.String(200), nullable=False)
    hq_city = db.Column(db.String(100), nullable=False)
    hq_state = db.Column(db.String(100), nullable=False)
    hq_country = db.Column(db.String(100), nullable=False)
    hq_telephone = db.Column(db.String(20), nullable=False)
    hq_fax = db.Column(db.String(20), nullable=True)  # Optional field

    regional_name = db.Column(db.String(100), nullable=True)  # Optional field for regional name
    regional_position = db.Column(db.String(100), nullable=True)  # Optional field for regional position
    regional_email = db.Column(db.String(100), nullable=True)  # Optional field for regional email
    regional_address = db.Column(db.String(200), nullable=True)  # Optional field for regional address
    regional_city = db.Column(db.String(100), nullable=True)  # Optional field for regional city
    regional_state = db.Column(db.String(100), nullable=True)  # Optional field for regional state
    regional_country = db.Column(db.String(100), nullable=True)  # Optional field for regional country
    regional_telephone = db.Column(db.String(20), nullable=True)  # Optional field for regional telephone
    regional_fax = db.Column(db.String(20), nullable=True)  # Optional field for regional fax

    def __init__(self, agency_registration_date, agency_registration_number, hq_name,
                 hq_position, hq_email, hq_address, hq_city, hq_state, hq_country,
                 hq_telephone, hq_fax=None, regional_name=None, regional_position=None,
                 regional_email=None, regional_address=None, regional_city=None,
                 regional_state=None, regional_country=None, regional_telephone=None,
                 regional_fax=None):
        self.agency_registration_date = agency_registration_date
        self.agency_registration_number = agency_registration_number
        self.hq_name = hq_name
        self.hq_position = hq_position
        self.hq_email = hq_email
        self.hq_address = hq_address
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country
        self.hq_telephone = hq_telephone
        self.hq_fax = hq_fax
        self.regional_name = regional_name
        self.regional_position = regional_position
        self.regional_email = regional_email
        self.regional_address = regional_address
        self.regional_city = regional_city
        self.regional_state = regional_state
        self.regional_country = regional_country
        self.regional_telephone = regional_telephone
        self.regional_fax = regional_fax

    def __repr__(self):
        return f"<MemberAccountAdministrator {self.hq_name}>"




