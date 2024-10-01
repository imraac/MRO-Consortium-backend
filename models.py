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


