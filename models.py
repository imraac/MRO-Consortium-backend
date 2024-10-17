
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import validates
# import re
# from datetime import datetime
# from flask_login import UserMixin

# db = SQLAlchemy()

# # User model
# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(129), nullable=False)
#     role = db.Column(db.String(50), default='user')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=True)

#     # Relationships
#     actions = db.relationship('UserAction', back_populates='user', cascade='all, delete-orphan')
#     # Specify the foreign_keys to clarify which column is used for the relationship
#     agencies = db.relationship('Agency', backref='user', foreign_keys='Agency.user_id', lazy=True)
#     founders = db.relationship('Founder', back_populates='user', cascade='all, delete-orphan')
#     board_directors = db.relationship('BoardDirector', back_populates='user', cascade='all, delete-orphan')
#     key_staff = db.relationship('KeyStaff', back_populates='user', cascade='all, delete-orphan')
#     consortiums = db.relationship('Consortium', back_populates='user', cascade='all, delete-orphan')
#     member_accounts = db.relationship('MemberAccountAdministrator', back_populates='user', cascade='all, delete-orphan')
#     consortium_applications = db.relationship('ConsortiumApplication', back_populates='user', cascade='all, delete-orphan')
   





#     @validates('email')
#     def validate_email(self, key, email):
#         regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
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
#             "created_at": self.created_at.isoformat(),
#             "agency_id": self.agency_id  
#         }



# # UserAction model
# class UserAction(db.Model):
#     __tablename__ = 'user_actions'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     action = db.Column(db.String(255), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

#     user = db.relationship('User', back_populates='actions')

#     def __repr__(self):
#         return f"<UserAction {self.id}: {self.action} by User {self.user_id} at {self.timestamp}>"

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'action': self.action,
#             'timestamp': self.timestamp.isoformat(),
#         }



# class Agency(db.Model):
#     __tablename__ = 'agencies'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
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

#     def __repr__(self):
#         return f"<Agency {self.id}: {self.full_name}>"

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
#             'commitment_to_principles': self.commitment_to_principles,
#             'user_id': self.user_id  # Include user_id if needed in the output
#         }



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


# class Consortium(db.Model):
#     __tablename__ = 'consortium'

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

#     def __repr__(self):
#         return f"<Consortium {self.id}: {self.active_year}>"

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'active_year': self.active_year,
#             'partner_ngos': self.partner_ngos,
#             'international_staff': self.international_staff,
#             'national_staff': self.national_staff,
#             'program_plans': self.program_plans,
#             'main_donors': self.main_donors,
#             'annual_budget': self.annual_budget,
#             'membership_type': self.membership_type
#         }


# class MemberAccountAdministrator(db.Model):
#     __tablename__ = 'member_account_administrator'
#     id = db.Column(db.Integer, primary_key=True)
#     member_name = db.Column(db.String(100), nullable=False)
#     member_email = db.Column(db.String(100), nullable=False)

#     # Updated fields from the frontend form
#     agency_registration_date = db.Column(db.Date, nullable=False)
#     agency_registration_number = db.Column(db.String(100), nullable=True)
#     hq_name = db.Column(db.String(100), nullable=False)
#     hq_position = db.Column(db.String(100), nullable=False)
#     hq_email = db.Column(db.String(100), nullable=False)
#     hq_address = db.Column(db.String(200), nullable=False)
#     hq_city = db.Column(db.String(100), nullable=False)
#     hq_state = db.Column(db.String(100), nullable=False)
#     hq_country = db.Column(db.String(100), nullable=False)
#     hq_telephone = db.Column(db.String(20), nullable=False)
#     hq_telephone2 = db.Column(db.String(20), nullable=True)
#     hq_fax = db.Column(db.String(20), nullable=True)

#     regional_same_as_hq = db.Column(db.Boolean, default=False)
#     regional_name = db.Column(db.String(100), nullable=True)
#     regional_position = db.Column(db.String(100), nullable=True)
#     regional_email = db.Column(db.String(100), nullable=True)
#     regional_address = db.Column(db.String(200), nullable=True)
#     regional_city = db.Column(db.String(100), nullable=True)
#     regional_state = db.Column(db.String(100), nullable=True)
#     regional_country = db.Column(db.String(100), nullable=True)
#     regional_telephone = db.Column(db.String(20), nullable=True)
#     regional_telephone2 = db.Column(db.String(20), nullable=True)
#     regional_fax = db.Column(db.String(20), nullable=True)


#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user = db.relationship('User', back_populates='member_accounts')

#     def __repr__(self):
#         return f"<MemberAccountAdministrator {self.id}: {self.hq_name}>"

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'member_name': self.member_name,
#             'member_email': self.member_email,
#             'agency_registration_date': self.agency_registration_date.isoformat(),  
#             'agency_registration_number': self.agency_registration_number,
#             'hq_name': self.hq_name,
#             'hq_position': self.hq_position,
#             'hq_email': self.hq_email,
#             'hq_address': self.hq_address,
#             'hq_city': self.hq_city,
#             'hq_state': self.hq_state,
#             'hq_country': self.hq_country,
#             'hq_telephone': self.hq_telephone,
#             'hq_telephone2': self.hq_telephone2,
#             'hq_fax': self.hq_fax,
#             'regional_same_as_hq': self.regional_same_as_hq,
#             'regional_name': self.regional_name,
#             'regional_position': self.regional_position,
#             'regional_email': self.regional_email,
#             'regional_address': self.regional_address,
#             'regional_city': self.regional_city,
#             'regional_state': self.regional_state,
#             'regional_country': self.regional_country,
#             'regional_telephone': self.regional_telephone,
#             'regional_telephone2': self.regional_telephone2,
#             'regional_fax': self.regional_fax
#         }







# class ConsortiumApplication(db.Model):
#     __tablename__ = 'consortium_applications'
    
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(100), nullable=False)
#     email_address = db.Column(db.String(100), nullable=False)
#     additional_accounts = db.Column(db.Integer, nullable=False)
#     mailing_list = db.Column(db.Text, nullable=True)  # You might want to process this as a list of emails
#     email_copy = db.Column(db.String(100), nullable=False)
#     documents = db.Column(db.JSON, nullable=True)  # Store document info, if needed
    
#     # Foreign key to associate with User
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # This assumes you have a users table

#     # Establish a relationship with User
#     user = db.relationship('User', back_populates='consortium_applications')
    
#     def as_dict(self):
#         return {
#             'id': self.id,
#             'full_name': self.full_name,
#             'email_address': self.email_address,
#             'additional_accounts': self.additional_accounts,
#             'mailing_list': self.mailing_list.splitlines() if self.mailing_list else [],  # Process mailing list
#             'email_copy': self.email_copy,
#             'documents': self.documents,
#             'user_id': self.user_id  # Include the user_id in the dict representation
#         }
    

# class ConsortiumMemberApplication(db.Model):
#     __tablename__ = 'consortium_member_applications'

#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(100), nullable=False)
#     email_address = db.Column(db.String(100), nullable=False)
#     additional_accounts = db.Column(db.Integer, nullable=False)
#     mailing_list = db.Column(db.Text, nullable=True)
#     email_copy = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to the User model

#     # Relationship
#     user = db.relationship('User', back_populates='consortium_member_applications')

#     def __repr__(self):
#         return f"<ConsortiumMemberApplication {self.full_name} - {self.email_address}>"

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'full_name': self.full_name,
#             'email_address': self.email_address,
#             'additional_accounts': self.additional_accounts,
#             'mailing_list': self.mailing_list,
#             'email_copy': self.email_copy,
#             'user_id': self.user_id
#         }
        

# class DocumentUpload(db.Model):
#     __tablename__ = 'document_uploads'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to associate with the User model
    
#     registration_certificate = db.Column(db.String(255), nullable=False)  # File path for the registration certificate
#     agency_profile = db.Column(db.String(255), nullable=False)  # File path for the agency profile
#     audit_report = db.Column(db.String(255), nullable=False)  # File path for the audit report
#     ngo_consortium_mandate = db.Column(db.String(255), nullable=False)  # File path for the NGO consortium mandate
#     icrc_code_of_conduct = db.Column(db.String(255), nullable=False)  # File path for the ICRC/Red Crescent code of conduct
    
#     upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp of the upload
#     status = db.Column(db.String(50), default='Pending', nullable=False)  # Status of the document ('Pending', 'Approved', 'Rejected')

#     # Relationship with the User model
#     user = db.relationship('User', back_populates='document_uploads')

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'username': self.user.username if self.user else "Unknown User",  # Include username
#             'email': self.user.email if self.user else "Unknown Email",  # Include email
#             'registration_certificate': self.registration_certificate,
#             'agency_profile': self.agency_profile,
#             'audit_report': self.audit_report,
#             'ngo_consortium_mandate': self.ngo_consortium_mandate,
#             'icrc_code_of_conduct': self.icrc_code_of_conduct,
#             'upload_date': self.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
#             'status': self.status
#         }
        
    





from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(129), nullable=False)
    role = db.Column(db.String(50), default='user')
    is_approved = db.Column(db.Boolean, default=False)  # Approval status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'))
    is_profile_complete = db.Column(db.Boolean, default=False)
    
    # Relationships
    actions = db.relationship('UserAction', back_populates='user', cascade='all, delete-orphan')
    agency = db.relationship('Agency', foreign_keys=[agency_id])

    founders = db.relationship('Founder', back_populates='user', cascade='all, delete-orphan')
    board_directors = db.relationship('BoardDirector', back_populates='user', cascade='all, delete-orphan')
    key_staff = db.relationship('KeyStaff', back_populates='user', cascade='all, delete-orphan')
    consortiums = db.relationship('Consortium', back_populates='user', cascade='all, delete-orphan')
    member_accounts = db.relationship('MemberAccountAdministrator', back_populates='user', cascade='all, delete-orphan')
    consortium_applications = db.relationship('ConsortiumApplication', back_populates='user', cascade='all, delete-orphan')
    consortium_member_applications = db.relationship('ConsortiumMemberApplication', back_populates='user', cascade='all, delete-orphan')
    document_uploads = db.relationship('DocumentUpload', back_populates='user', cascade='all, delete-orphan')

    @validates('email')
    def validate_email(self, key, email):
        regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
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
            "is_approved": self.is_approved,  # Include approval status in dict
            "created_at": self.created_at.isoformat(),
            "agency_id": self.agency_id,
            "is_profile_complete": self.is_profile_complete,
        }


# UserAction model
class UserAction(db.Model):
    __tablename__ = 'user_actions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='actions')

    def __repr__(self):
        return f"<UserAction {self.id}: {self.action} by User {self.user_id} at {self.timestamp}>"

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'timestamp': self.timestamp.isoformat(),
        }



class Agency(db.Model):
    __tablename__ = 'agencies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
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

    def __repr__(self):
        return f"<Agency {self.id}: {self.full_name}>"

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
            'commitment_to_principles': self.commitment_to_principles,
            'user_id': self.user_id  # Include user_id if needed in the output
        }



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

    def __repr__(self):
        return f"<Consortium {self.id}: {self.active_year}>"

    def as_dict(self):
        return {
            'id': self.id,
            'active_year': self.active_year,
            'partner_ngos': self.partner_ngos,
            'international_staff': self.international_staff,
            'national_staff': self.national_staff,
            'program_plans': self.program_plans,
            'main_donors': self.main_donors,
            'annual_budget': self.annual_budget,
            'membership_type': self.membership_type
        }


class MemberAccountAdministrator(db.Model):
    __tablename__ = 'member_account_administrator'
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(100), nullable=False)
    member_email = db.Column(db.String(100), nullable=False)

    # Updated fields from the frontend form
    agency_registration_date = db.Column(db.Date, nullable=False)
    agency_registration_number = db.Column(db.String(100), nullable=True)
    hq_name = db.Column(db.String(100), nullable=False)
    hq_position = db.Column(db.String(100), nullable=False)
    hq_email = db.Column(db.String(100), nullable=False)
    hq_address = db.Column(db.String(200), nullable=False)
    hq_city = db.Column(db.String(100), nullable=False)
    hq_state = db.Column(db.String(100), nullable=False)
    hq_country = db.Column(db.String(100), nullable=False)
    hq_telephone = db.Column(db.String(20), nullable=False)
    hq_telephone2 = db.Column(db.String(20), nullable=True)
    hq_fax = db.Column(db.String(20), nullable=True)

    regional_same_as_hq = db.Column(db.Boolean, default=False)
    regional_name = db.Column(db.String(100), nullable=True)
    regional_position = db.Column(db.String(100), nullable=True)
    regional_email = db.Column(db.String(100), nullable=True)
    regional_address = db.Column(db.String(200), nullable=True)
    regional_city = db.Column(db.String(100), nullable=True)
    regional_state = db.Column(db.String(100), nullable=True)
    regional_country = db.Column(db.String(100), nullable=True)
    regional_telephone = db.Column(db.String(20), nullable=True)
    regional_telephone2 = db.Column(db.String(20), nullable=True)
    regional_fax = db.Column(db.String(20), nullable=True)


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='member_accounts')

    def __repr__(self):
        return f"<MemberAccountAdministrator {self.id}: {self.hq_name}>"

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'member_name': self.member_name,
            'member_email': self.member_email,
            'agency_registration_date': self.agency_registration_date.isoformat(),  
            'agency_registration_number': self.agency_registration_number,
            'hq_name': self.hq_name,
            'hq_position': self.hq_position,
            'hq_email': self.hq_email,
            'hq_address': self.hq_address,
            'hq_city': self.hq_city,
            'hq_state': self.hq_state,
            'hq_country': self.hq_country,
            'hq_telephone': self.hq_telephone,
            'hq_telephone2': self.hq_telephone2,
            'hq_fax': self.hq_fax,
            'regional_same_as_hq': self.regional_same_as_hq,
            'regional_name': self.regional_name,
            'regional_position': self.regional_position,
            'regional_email': self.regional_email,
            'regional_address': self.regional_address,
            'regional_city': self.regional_city,
            'regional_state': self.regional_state,
            'regional_country': self.regional_country,
            'regional_telephone': self.regional_telephone,
            'regional_telephone2': self.regional_telephone2,
            'regional_fax': self.regional_fax
        }







class ConsortiumApplication(db.Model):
    __tablename__ = 'consortium_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    additional_accounts = db.Column(db.Integer, nullable=False)
    mailing_list = db.Column(db.Text, nullable=True)  # You might want to process this as a list of emails
    email_copy = db.Column(db.String(100), nullable=False)
    
    # Foreign key to associate with User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # This assumes you have a users table

    # Establish a relationship with User
    user = db.relationship('User', back_populates='consortium_applications')
    
    def as_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email_address': self.email_address,
            'additional_accounts': self.additional_accounts,
            'mailing_list': self.mailing_list.splitlines() if self.mailing_list else [],  # Process mailing list
            'email_copy': self.email_copy,
            'user_id': self.user_id  # Include the user_id in the dict representation
        }
    






class ConsortiumMemberApplication(db.Model):
    __tablename__ = 'consortium_member_applications'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    additional_accounts = db.Column(db.Integer, nullable=False)
    mailing_list = db.Column(db.Text, nullable=True)
    email_copy = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to the User model

    # Relationship
    user = db.relationship('User', back_populates='consortium_member_applications')

    def __repr__(self):
        return f"<ConsortiumMemberApplication {self.full_name} - {self.email_address}>"

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email_address': self.email_address,
            'additional_accounts': self.additional_accounts,
            'mailing_list': self.mailing_list,
            'email_copy': self.email_copy,
            'user_id': self.user_id
        }
        
        
        

# class DocumentUpload(db.Model):
#     __tablename__ = 'document_uploads'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key for User
#     full_name = db.Column(db.String(100), nullable=False)
#     email_address = db.Column(db.String(100), nullable=False)
#     additional_accounts = db.Column(db.Integer, nullable=False)
#     mailing_list = db.Column(db.Text, nullable=False)
#     email_copy = db.Column(db.String(100), nullable=False)
    
#     registration_certificate = db.Column(db.String(200), nullable=False)  # Path or filename of the uploaded file
#     agency_profile = db.Column(db.String(200), nullable=False)
#     audit_report = db.Column(db.String(200), nullable=False)
#     ngo_consortium_mandate = db.Column(db.String(200), nullable=False)
#     icrc_code_of_conduct = db.Column(db.String(200), nullable=False)

#     # Relationship with User model
#     user = db.relationship('User', back_populates='document_uploads')

#     def __repr__(self):
#         return f'<DocumentUpload {self.full_name}>'

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'full_name': self.full_name,
#             'email_address': self.email_address,
#             'additional_accounts': self.additional_accounts,
#             'mailing_list': self.mailing_list,
#             'email_copy': self.email_copy,
#             'registration_certificate': self.registration_certificate,
#             'agency_profile': self.agency_profile,
#             'audit_report': self.audit_report,
#             'ngo_consortium_mandate': self.ngo_consortium_mandate,
#             'icrc_code_of_conduct': self.icrc_code_of_conduct
#         }        
        
        
        
        


class DocumentUpload(db.Model):
    __tablename__ = 'document_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to associate with the User model
    
    registration_certificate = db.Column(db.String(255), nullable=False)  # File path for the registration certificate
    agency_profile = db.Column(db.String(255), nullable=False)  # File path for the agency profile
    audit_report = db.Column(db.String(255), nullable=False)  # File path for the audit report
    ngo_consortium_mandate = db.Column(db.String(255), nullable=False)  # File path for the NGO consortium mandate
    icrc_code_of_conduct = db.Column(db.String(255), nullable=False)  # File path for the ICRC/Red Crescent code of conduct
    
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp of the upload
    status = db.Column(db.String(50), default='Pending', nullable=False)  # Status of the document ('Pending', 'Approved', 'Rejected')

    # Relationship with the User model
    user = db.relationship('User', back_populates='document_uploads')

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else "Unknown User",  # Include username
            'email': self.user.email if self.user else "Unknown Email",  # Include email
            'registration_certificate': self.registration_certificate,
            'agency_profile': self.agency_profile,
            'audit_report': self.audit_report,
            'ngo_consortium_mandate': self.ngo_consortium_mandate,
            'icrc_code_of_conduct': self.icrc_code_of_conduct,
            'upload_date': self.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }