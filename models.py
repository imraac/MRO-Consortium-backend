# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import validates
# import re
# from datetime import datetime

# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'users'  

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(129), nullable=False)
#     role = db.Column(db.String(50), default='user')
#     created_at = db.Column(db.DateTime, default=db.func.now())
#     agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=True)  # Corrected ForeignKey reference

#     # Define a relationship to the Agency
#     agencies = db.relationship('Agency', back_populates='user', foreign_keys=[agency_id])  # Use agency_id instead

#     # Other relationships
#     contact_details = db.relationship('ContactDetail', back_populates='user')
#     founders = db.relationship('Founder', back_populates='user')
#     board_directors = db.relationship('BoardDirector', back_populates='user')
#     key_staff = db.relationship('KeyStaff', back_populates='user')
#     consortiums = db.relationship('Consortium', back_populates='user')
#     member_accounts = db.relationship('MemberAccountAdministrator', back_populates='user')

#     @validates('email')
#     def validate_email(self, key, email):
#         regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         if not re.match(regex, email):
#             raise ValueError("Invalid email address")
#         return email

#     def __repr__(self):
#         return f"<User {self.id}: {self.username}>"

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "username": self.username,
#             "email": self.email,
#             "role": self.role,
#             "created_at": str(self.created_at),
#             "agency_id": self.agency_id  # Include agency_id if needed
#         }


# class Agency(db.Model):
#     __tablename__ = 'agencies'
    
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

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # User foreign key

#     # Define a relationship with User
#     user = db.relationship('User', back_populates='agencies')  # Corrected to use agencies relationship without foreign_keys

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


# # ContactDetail Model
# class ContactDetail(db.Model):
#     __tablename__ = 'contact_detail'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     contact = db.Column(db.String(100), nullable=False)
#     clan = db.Column(db.String(100), nullable=True)
#     role = db.Column(db.String(50), nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user = db.relationship('User', back_populates='contact_details')

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'contact': self.contact,
#             'clan': self.clan,
#             'role': self.role
#         }

# # Founder Model
# class Founder(db.Model):
#     __tablename__ = 'founder'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     contact = db.Column(db.String(100), nullable=False)
#     clan = db.Column(db.String(100), nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user = db.relationship('User', back_populates='founders')

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'contact': self.contact,
#             'clan': self.clan
#         }

# # BoardDirector Model
# class BoardDirector(db.Model):
#     __tablename__ = 'board_director'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     contact = db.Column(db.String(100), nullable=False)
#     clan = db.Column(db.String(100), nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user = db.relationship('User', back_populates='board_directors')

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'contact': self.contact,
#             'clan': self.clan
#         }

# # KeyStaff Model
# class KeyStaff(db.Model):
#     __tablename__ = 'key_staff'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     contact = db.Column(db.String(100), nullable=False)
#     clan = db.Column(db.String(100), nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user = db.relationship('User', back_populates='key_staff')

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'contact': self.contact,
#             'clan': self.clan
#         }

# # Consortium Model
# class Consortium(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     active_year = db.Column(db.String(4), nullable=False)
#     partner_ngos = db.Column(db.Text, nullable=False)
#     international_staff = db.Column(db.Integer, nullable=False)
#     national_staff = db.Column(db.Integer, nullable=False)
#     program_plans = db.Column(db.Text, nullable=False)
#     main_donors = db.Column(db.Text, nullable=False)
#     annual_budget = db.Column(db.String(20), nullable=False)
#     membership_type = db.Column(db.String(50), nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user = db.relationship('User', back_populates='consortiums')

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'active_year': self.active_year,
#             'user_id': self.user_id
#         }

# # MemberAccountAdministrator Model
# class MemberAccountAdministrator(db.Model):
#     __tablename__ = 'member_account_administrator'  
#     id = db.Column(db.Integer, primary_key=True)
#     agency_registration_date = db.Column(db.Date, nullable=False)
#     agency_registration_number = db.Column(db.String(100), nullable=False)
#     hq_name = db.Column(db.String(100), nullable=False)
#     hq_position = db.Column(db.String(100), nullable=False)
#     hq_email = db.Column(db.String(100), nullable=False)
#     hq_address = db.Column(db.String(200), nullable=False)
#     hq_city = db.Column(db.String(100), nullable=False)
#     hq_state = db.Column(db.String(100), nullable=False)
#     hq_country = db.Column(db.String(100), nullable=False)
#     hq_telephone = db.Column(db.String(20), nullable=False)
#     hq_fax = db.Column(db.String(20), nullable=True)
#     regional_name = db.Column(db.String(100), nullable=True)
#     regional_position = db.Column(db.String(100), nullable=True)
#     regional_email = db.Column(db.String(100), nullable=True)
#     regional_address = db.Column(db.String(200), nullable=True)
#     regional_city = db.Column(db.String(100), nullable=True)
#     regional_state = db.Column(db.String(100), nullable=True)
#     regional_country = db.Column(db.String(100), nullable=True)
#     regional_telephone = db.Column(db.String(20), nullable=True)
#     regional_fax = db.Column(db.String(20), nullable=True)


 
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Add this line if relevant
#     user = db.relationship('User', back_populates='member_accounts')  # Create this relationship in the User model as well


#     def __repr__(self):
#         return f"<MemberAccountAdministrator {self.hq_name}>"

# # Helper function to save a model to the database
# def save_to_db(model):
#     db.session.add(model)
#     db.session.commit()


# def create_contact_detail(name, contact, clan, role, user_id):
#     new_contact_detail = ContactDetail(name=name, contact=contact, clan=clan, role=role, user_id=user_id)
#     save_to_db(new_contact_detail)

# def create_founder(name, contact, clan, user_id):
#     new_founder = Founder(name=name, contact=contact, clan=clan, user_id=user_id)
#     save_to_db(new_founder)

# def create_board_director(name, contact, clan, user_id):
#     new_board_director = BoardDirector(name=name, contact=contact, clan=clan, user_id=user_id)
#     save_to_db(new_board_director)

# def create_key_staff(name, contact, clan, user_id):
#     new_key_staff = KeyStaff(name=name, contact=contact, clan=clan, user_id=user_id)
#     save_to_db(new_key_staff)

# def create_consortium(data, user_id):
#     new_consortium = Consortium(user_id=user_id, **data)
#     save_to_db(new_consortium)


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(129), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=db.func.now())
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=True)  

    # Define a relationship to the Agency
    agency = db.relationship('Agency', back_populates='users', foreign_keys=[agency_id])

    # Other relationships
    contact_details = db.relationship('ContactDetail', back_populates='user')
    founders = db.relationship('Founder', back_populates='user')
    board_directors = db.relationship('BoardDirector', back_populates='user')
    key_staff = db.relationship('KeyStaff', back_populates='user')
    consortiums = db.relationship('Consortium', back_populates='user')
    member_accounts = db.relationship('MemberAccountAdministrator', back_populates='user')

    @validates('email')
    def validate_email(self, key, email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": str(self.created_at),
            "agency_id": self.agency_id  
        }


class Agency(db.Model):
    __tablename__ = 'agencies'
    
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

    users = db.relationship('User', back_populates='agency')  # Use 'users' to denote multiple User instances

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


# ContactDetail Model
class ContactDetail(db.Model):
    __tablename__ = 'contact_detail'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    clan = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='contact_details')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'clan': self.clan,
            'role': self.role
        }

# Founder Model
class Founder(db.Model):
    __tablename__ = 'founder'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    clan = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='founders')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'clan': self.clan
        }

# BoardDirector Model
class BoardDirector(db.Model):
    __tablename__ = 'board_director'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    clan = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='board_directors')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'clan': self.clan
        }

# KeyStaff Model
class KeyStaff(db.Model):
    __tablename__ = 'key_staff'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    clan = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='key_staff')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'clan': self.clan
        }

# Consortium Model
class Consortium(db.Model):
    __tablename__ = 'consortium'

    id = db.Column(db.Integer, primary_key=True)
    active_year = db.Column(db.String(4), nullable=False)
    partner_ngos = db.Column(db.Text, nullable=False)
    international_staff = db.Column(db.Integer, nullable=False)
    national_staff = db.Column(db.Integer, nullable=False)
    program_plans = db.Column(db.Text, nullable=False)
    main_donors = db.Column(db.Text, nullable=False)
    annual_budget = db.Column(db.String(20), nullable=False)
    membership_type = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='consortiums')

    def as_dict(self):
        return {
            'id': self.id,
            'active_year': self.active_year,
            'user_id': self.user_id
        }

# MemberAccountAdministrator Model
class MemberAccountAdministrator(db.Model):
    __tablename__ = 'member_account_administrator'  
    id = db.Column(db.Integer, primary_key=True)
    agency_registration_date = db.Column(db.Date, nullable=False)
    agency_registration_number = db.Column(db.String(100), nullable=False)
    hq_name = db.Column(db.String(100), nullable=False)
    hq_position = db.Column(db.String(100), nullable=False)
    hq_email = db.Column(db.String(100), nullable=False)
    hq_address = db.Column(db.String(200), nullable=False)
    hq_city = db.Column(db.String(100), nullable=False)
    hq_state = db.Column(db.String(100), nullable=False)
    hq_country = db.Column(db.String(100), nullable=False)
    hq_telephone = db.Column(db.String(20), nullable=False)
    hq_fax = db.Column(db.String(20), nullable=True)
    regional_name = db.Column(db.String(100), nullable=True)
    regional_position = db.Column(db.String(100), nullable=True)
    regional_email = db.Column(db.String(100), nullable=True)
    regional_address = db.Column(db.String(200), nullable=True)
    regional_city = db.Column(db.String(100), nullable=True)
    regional_state = db.Column(db.String(100), nullable=True)
    regional_country = db.Column(db.String(100), nullable=True)
    regional_telephone = db.Column(db.String(20), nullable=True)
    regional_fax = db.Column(db.String(20), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='member_accounts')

    def as_dict(self):
        return {
            'id': self.id,
            'agency_registration_date': str(self.agency_registration_date),
            'agency_registration_number': self.agency_registration_number,
            'hq_name': self.hq_name,
            'hq_position': self.hq_position,
            'hq_email': self.hq_email,
            'hq_address': self.hq_address,
            'hq_city': self.hq_city,
            'hq_state': self.hq_state,
            'hq_country': self.hq_country,
            'hq_telephone': self.hq_telephone,
            'hq_fax': self.hq_fax,
            'regional_name': self.regional_name,
            'regional_position': self.regional_position,
            'regional_email': self.regional_email,
            'regional_address': self.regional_address,
            'regional_city': self.regional_city,
            'regional_state': self.regional_state,
            'regional_country': self.regional_country,
            'regional_telephone': self.regional_telephone,
            'regional_fax': self.regional_fax
        }
