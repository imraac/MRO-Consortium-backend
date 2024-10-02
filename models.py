from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(129), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=db.func.now())

  
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'), nullable=True)
    agency = db.relationship('Agency', back_populates='users', foreign_keys=[agency_id])

    contact_details = db.relationship('ContactDetail', back_populates='user')
    founders = db.relationship('Founder', back_populates='user')
    board_directors = db.relationship('BoardDirector', back_populates='user')
    key_staff = db.relationship('KeyStaff', back_populates='user')

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
    __tablename__ = 'agency'  

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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Reverse relationships
    users = db.relationship('User', back_populates='agency', foreign_keys=[User.agency_id])

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
# ContactDetail model
class ContactDetail(db.Model):
    __tablename__ = 'contact_detail'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    clan = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    user = db.relationship('User', back_populates='contact_details')  

    def _init_(self, name, contact, clan, role):
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


# Founder model
class Founder(db.Model):
    __tablename__ = 'founder'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    clan = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    user = db.relationship('User', back_populates='founders')  

    def _init_(self, name, contact, clan, user_id):
        self.name = name
        self.contact = contact
        self.clan = clan
        self.user_id = user_id

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



def save_to_db(model):
    db.session.add(model)
    db.session.commit()


def create_founder(name, contact, clan, user_id):
    new_founder = Founder(name=name, contact=contact, clan=clan, user_id=user_id)
    save_to_db(new_founder)