

from flask import Flask, request, jsonify, make_response, session
from models import db, Founder, Agency, User ,UserAction ,BoardDirector,KeyStaff,Consortium ,MemberAccountAdministrator,ConsortiumApplication ,ConsortiumMemberApplication,DocumentUpload,LoginHistory
from flask import Flask, request, jsonify
import jwt
from flask_jwt_extended import get_jwt
from config import Config
from flask import send_from_directory
from flask_login import  login_required,  current_user,LoginManager
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime,timedelta
from flask_migrate import Migrate
import logging
import os
from werkzeug.utils import secure_filename
from flask import current_app
from file_utils import save_file_to_directory 
from itsdangerous import URLSafeSerializer
from flask_mail import Mail , Message
import pytz
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  
UPLOAD_DIRECTORY = os.path.join(os.getcwd(), 'uploads')  
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 16 MB
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
login_manager = LoginManager(app)  
login_manager.init_app(app)
migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

mail = Mail(app)
# with app.app_context():
    # db.create_all()

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['SESSION_COOKIE_HTTPONLY'] = True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


class LoginHistoryResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()  
        login_history = LoginHistory.query.filter_by(user_id=user_id).order_by(LoginHistory.login_time.desc()).all()
        kenya_timezone = pytz.timezone("Africa/Nairobi")
        utc_timezone = pytz.UTC

        history_data = []
        for entry in login_history:
            login_time_utc = entry.login_time.replace(tzinfo=utc_timezone)
            login_time_kenya = login_time_utc.astimezone(kenya_timezone).strftime("%A, %d %B %Y, %I:%M:%S %p")
            
            logout_time_kenya = (
                entry.logout_time.replace(tzinfo=utc_timezone).astimezone(kenya_timezone).strftime("%A, %d %B %Y, %I:%M:%S %p")
                if entry.logout_time else None
            )
            
            history_data.append({
                "login_time": login_time_kenya,
                "logout_time": logout_time_kenya
            })

        return jsonify(history_data)
class Users(Resource):
    def post(self):
        data = request.get_json()
        email = User.query.filter_by(email=data.get('email')).first()
        if email:
            return make_response({"message": "Email already taken"}, 422)

        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=bcrypt.generate_password_hash(data.get("password")).decode('utf-8'),
            role=data.get("role", "user"),
            agency_id=None
        )

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return make_response({
            "user": new_user.to_dict(),
            "access_token": access_token,
            "success": True,
            "message": "User has been created successfully"
        }, 201)
    def get(self):
        users = User.query.all()
        
        users_list = [user.to_dict() for user in users]

        return make_response({
            "users": users_list,
            "success": True,
            "message": "Users retrieved successfully"
        }, 200)




@app.route('/users/list', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [user.to_dict() for user in users]

    return jsonify({
        "users": users_list,
        "success": True,
        "message": "Users retrieved successfully"
    })


from datetime import datetime

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            session['user_id'] = user.id 

            login_entry = LoginHistory(user_id=user.id, login_time=datetime.utcnow())
            db.session.add(login_entry)
            db.session.commit()

            document = DocumentUpload.query.filter_by(user_id=user.id).first()
            document_status = document.status if document else "Pending"

            return make_response({
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                    "is_approved": user.is_approved,
                    "document_status": document_status
                },
                "access_token": access_token,
                "success": True,
                "message": "Login successful"
            }, 200)
        
        return make_response({"message": "Invalid credentials"}, 401)







blacklist = set()

class Logout(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()["jti"]
            
            blacklist.add(jti)
            
            session.pop('user_id', None)
            
            return {"message": "Logout successful"}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist



class VerifyToken(Resource):
    @jwt_required()
    def post(self):
        current_user = get_current_user()  
        if current_user:
            return make_response({
                "user": current_user.to_dict(),
                "success": True,
                "message": "Token is valid"
            }, 200)
        return make_response({"message": "Invalid token"}, 401)
# 


@app.route('/agency', methods=['POST'])
@jwt_required() 
def add_agency():
   
    current_user_id = get_jwt_identity()  
   

    
    data = request.get_json()
    
    try:
       
        agency = Agency(
            full_name=data['full_name'],
            acronym=data.get('acronym'),  
            description=data['description'],
            mission_statement=data['mission_statement'],
            website=data['website'],
            is_ngo=data['is_ngo'],
            years_operational=data['years_operational'],
            reason_for_joining=data['reason_for_joining'],
            willing_to_participate=data['willing_to_participate'],
            commitment_to_principles=data['commitment_to_principles'],
        )
        
        agency.user_id = current_user_id  
        db.session.add(agency)
        db.session.commit()

        
        response_data = {
            "id": agency.id,
            "full_name": agency.full_name,
            "acronym": agency.acronym,
            "description": agency.description,
            "mission_statement": agency.mission_statement,
            "website": agency.website,
            "is_ngo": agency.is_ngo,
            "years_operational": agency.years_operational,
            "reason_for_joining": agency.reason_for_joining,
            "willing_to_participate": agency.willing_to_participate,
            "commitment_to_principles": agency.commitment_to_principles,
            "user_id": agency.user_id  
        }

        return jsonify({"message": "Agency added successfully!", "agency": response_data}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/agency', methods=['GET'])
@jwt_required()
def get_agencies():
    try:
        current_user_id = get_jwt_identity()

        agencies = Agency.query.filter_by(user_id=current_user_id).all()

        agencies_list = [{
            "id": agency.id,
            "full_name": agency.full_name,
            "acronym": agency.acronym,
            "description": agency.description,
            "mission_statement": agency.mission_statement,
            "website": agency.website,
            "is_ngo": agency.is_ngo,
            "years_operational": agency.years_operational,
            "reason_for_joining": agency.reason_for_joining,
            "willing_to_participate": agency.willing_to_participate,
            "commitment_to_principles": agency.commitment_to_principles,
            "user_id": agency.user_id
        } for agency in agencies]

        return jsonify({
            "message": "Agencies retrieved successfully!",
            "agencies": agencies_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500








@app.route('/agencies', methods=['GET'])
@jwt_required()
def get_all_agencies():
    try:
        agencies = Agency.query.all()

        agencies_list = [{
            "id": agency.id,
            "full_name": agency.full_name,
            "acronym": agency.acronym,
            "description": agency.description,
            "mission_statement": agency.mission_statement,
            "website": agency.website,
            "is_ngo": agency.is_ngo,
            "years_operational": agency.years_operational,
            "reason_for_joining": agency.reason_for_joining,
            "willing_to_participate": agency.willing_to_participate,
            "commitment_to_principles": agency.commitment_to_principles,
            "user_id": agency.user_id
        } for agency in agencies]

        return jsonify({
            "message": "All agencies retrieved successfully!",
            "agencies": agencies_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/agency/<int:agency_id>', methods=['DELETE'])
@jwt_required()  
def delete_agency(agency_id):
    user_id = get_jwt_identity()  
    agency = Agency.query.filter_by(id=agency_id, user_id=user_id).first_or_404()  
    db.session.delete(agency)
    db.session.commit()
    return jsonify({"message": "Agency deleted successfully!"}), 200


@app.route('/user/actions', methods=['GET'])
@jwt_required()  
def get_user_actions():
    current_user = get_current_user()  
    actions = UserAction.query.filter_by(user_id=current_user.id).all()
    return jsonify([action.as_dict() for action in actions]), 200



@app.route('/agency', methods=['PUT'])
@jwt_required()
def update_agency():
    try:
        current_user = get_current_user()  
        print(f"Current user ID: {current_user.id}")  

        if not request.is_json:
            return jsonify({"error": "Request must be in JSON format"}), 400

        data = request.get_json()

        def parse_boolean(value):
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                return value.lower() in ['true', '1', 't', 'y', 'yes']
            return False

        agency = Agency.query.filter_by(user_id=current_user.id).first()

        if not agency:
            print(f"No agency found for user {current_user.id}")  
            return jsonify({"message": "Agency not found or not authorized"}), 404

        print(f"Updating agency: {agency.id}, {agency.full_name}")

        agency.full_name = data.get('full_name', agency.full_name)
        agency.acronym = data.get('acronym', agency.acronym)
        agency.description = data.get('description', agency.description)
        agency.mission_statement = data.get('mission_statement', agency.mission_statement)
        agency.website = data.get('website', agency.website)
        
        agency.is_ngo = parse_boolean(data.get('is_ngo', agency.is_ngo))
        agency.years_operational = data.get('years_operational', agency.years_operational)
        agency.reason_for_joining = data.get('reason_for_joining', agency.reason_for_joining)
        agency.willing_to_participate = parse_boolean(data.get('willing_to_participate', agency.willing_to_participate))
        agency.commitment_to_principles = parse_boolean(data.get('commitment_to_principles', agency.commitment_to_principles))

        db.session.commit()

        updated_agency = Agency.query.get(agency.id)

        return jsonify({
            "message": "Agency updated successfully!",
            "agency": updated_agency.as_dict()
        }), 200

    except Exception as e:
        db.session.rollback()  
        print(f"Error during agency update: {str(e)}")  
        return jsonify({"error": str(e)}), 500
# 




@app.route('/log-action', methods=['POST'])
@jwt_required()  
def log_user_action():
    current_user = get_current_user()  
    data = request.get_json()

    try:
        action = UserAction(
            user_id=current_user.id,  
            action_type=data['action_type'],
            action_description=data['action_description'],
            timestamp=datetime.utcnow()
        )

        db.session.add(action)
        db.session.commit()

        return jsonify({"message": "Action logged successfully!"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/founders', methods=['POST'])
@jwt_required()  
def create_founder():
    current_user_id = get_jwt_identity()  
  
    
    data = request.json
    new_founder = Founder(
        name=data['name'],
        contact=data['contact'],
        clan=data['clan'],
        user_id=current_user_id  
    )
    db.session.add(new_founder)
    db.session.commit()

    user_action = UserAction(user_id=current_user_id, action="Created a founder")
    db.session.add(user_action)
    db.session.commit()

    return jsonify(new_founder.as_dict()), 201







@app.route('/founders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required() 
def handle_founder(id):
    
    current_user_id = get_jwt_identity()
   
    founder = Founder.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(founder.as_dict()), 200

    elif request.method == 'PUT':
        data = request.json
        founder.name = data.get('name', founder.name)
        founder.contact = data.get('contact', founder.contact)
        founder.clan = data.get('clan', founder.clan)
        founder.user_id = current_user_id 

        db.session.commit()
        return jsonify(founder.as_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(founder)
        db.session.commit()
        return jsonify({"message": "Founder deleted"}), 200








@app.route('/board-directors', methods=['GET', 'POST'])
@jwt_required() 
def handle_board_directors():
    current_user_id = get_jwt_identity()  
    print(f"User ID: {current_user_id}")  
    if current_user_id is None:
        return jsonify({"msg": "User ID not found in token."}), 401 

    if request.method == 'POST':
        data = request.json
        
        new_board_director = BoardDirector(
            name=data.get('name'),
            contact=data.get('contact'),
            clan=data.get('clan'),
            user_id=current_user_id  
        )

        db.session.add(new_board_director)
        db.session.commit()
        return jsonify(new_board_director.as_dict()), 201

    elif request.method == 'GET':
        directors = BoardDirector.query.all()
        return jsonify([director.as_dict() for director in directors]), 200


@app.route('/board-directors/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_board_director(id):
    director = BoardDirector.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(director.as_dict()), 200

    elif request.method == 'PUT':
        data = request.json
        director.name = data.get('name', director.name)
        director.contact = data.get('contact', director.contact)
        director.clan = data.get('clan', director.clan)
        director.user_id = data.get('user_id', director.user_id)

        db.session.commit()
        return jsonify(director.as_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(director)
        db.session.commit()
        return jsonify({"message": "Board Director deleted"}), 200


@app.route('/key-staff', methods=['GET', 'POST'])
@jwt_required()
def handle_key_staff():
    current_user_id = get_jwt_identity()
  

    if request.method == 'POST':
        data = request.json
        
        
        if not all(key in data for key in ('name', 'contact', 'clan')):
            return jsonify({"msg": "Missing required fields"}), 400
        
        new_staff = KeyStaff(
            name=data.get('name'),
            contact=data.get('contact'),
            clan=data.get('clan'),
            user_id=current_user_id
        )
        try:
            db.session.add(new_staff)
            db.session.commit()
            return jsonify(new_staff.as_dict()), 201
        except Exception as e:
            db.session.rollback()  
            return jsonify({"msg": str(e)}), 500  


@app.route('/key-staff/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_key_staff_member(id):
    staff = KeyStaff.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(staff.as_dict()), 200

    elif request.method == 'PUT':
        data = request.json
        staff.name = data.get('name', staff.name)
        staff.contact = data.get('contact', staff.contact)
        staff.clan = data.get('clan', staff.clan)
        staff.user_id = data.get('user_id', staff.user_id)

        db.session.commit()
        return jsonify(staff.as_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(staff)
        db.session.commit()
        return jsonify({"message": "Key Staff deleted"}), 200




@app.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(newToken=new_token), 200




@app.route('/consortium', methods=['POST'])
@jwt_required() 
def create_consortium():
    current_user_id = get_jwt_identity()  


    data = request.json
    new_consortium = Consortium(
        active_year=data['activeYear'],
        partner_ngos=data['partnerNGOs'],
        international_staff=data['internationalStaff'],
        national_staff=data['nationalStaff'],
        program_plans=data['programPlans'],
        main_donors=data['mainDonors'],
        annual_budget=data['annualBudget'],
        membership_type=data['membershipType'],
        user_id=current_user_id  
    )
    
    db.session.add(new_consortium)
    db.session.commit()
    
    return jsonify(new_consortium.as_dict()), 201

@app.route('/consortium', methods=['GET'])
@jwt_required()  
def get_consortia():
    current_user_id = get_jwt_identity()  


    consortia = Consortium.query.filter_by(user_id=current_user_id).all()
    return jsonify([consortium.as_dict() for consortium in consortia]), 200









@app.route('/member-account', methods=['POST'])
@jwt_required()  
def create_member_account():
    data = request.json
    current_user_id = get_jwt_identity()  
    
    try:
        new_member = MemberAccountAdministrator(
            member_name=data['member_name'],
            member_email=data['member_email'],
            agency_registration_date=datetime.fromisoformat(data['agency_registration_date']),
            agency_registration_number=data.get('agency_registration_number'),  
            hq_name=data['hq_name'],
            hq_position=data['hq_position'],
            hq_email=data['hq_email'],
            hq_address=data['hq_address'],
            hq_city=data['hq_city'],
            hq_state=data['hq_state'],
            hq_country=data['hq_country'],
            hq_telephone=data['hq_telephone'],
            hq_telephone2=data.get('hq_telephone2'),  
            hq_fax=data.get('hq_fax'), 
            regional_same_as_hq=data.get('regional_same_as_hq', False),  
            regional_name=data.get('regional_name'),  
            regional_position=data.get('regional_position'), 
            regional_email=data.get('regional_email'), 
            regional_address=data.get('regional_address'),
            regional_city=data.get('regional_city'),  
            regional_state=data.get('regional_state'), 
            regional_country=data.get('regional_country'), 
            regional_telephone=data.get('regional_telephone'), 
            regional_telephone2=data.get('regional_telephone2'), 
            regional_fax=data.get('regional_fax'),  
            user_id=current_user_id  
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify(new_member.as_dict()), 201
    except Exception as e:

        return jsonify({'error': str(e)}), 400



@app.route('/member-account/<int:id>', methods=['PUT'])
@jwt_required() 
def update_member_account(id):
    data = request.json
    member = MemberAccountAdministrator.query.get_or_404(id)
    
    current_user_id = get_jwt_identity()  
    
    if member.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access.'}), 403

    member.member_name = data.get('member_name', member.member_name)
    member.member_email = data.get('member_email', member.member_email)
    member.agency_registration_date = datetime.fromisoformat(data.get('agency_registration_date', member.agency_registration_date.isoformat()))
    member.agency_registration_number = data.get('agency_registration_number', member.agency_registration_number)
    member.hq_name = data.get('hq_name', member.hq_name)
    member.hq_position = data.get('hq_position', member.hq_position)
    member.hq_email = data.get('hq_email', member.hq_email)
    member.hq_address = data.get('hq_address', member.hq_address)
    member.hq_city = data.get('hq_city', member.hq_city)
    member.hq_state = data.get('hq_state', member.hq_state)
    member.hq_country = data.get('hq_country', member.hq_country)
    member.hq_telephone = data.get('hq_telephone', member.hq_telephone)
    member.hq_telephone2 = data.get('hq_telephone2', member.hq_telephone2)
    member.hq_fax = data.get('hq_fax', member.hq_fax)

    member.regional_same_as_hq = data.get('regional_same_as_hq', member.regional_same_as_hq)
    member.regional_name = data.get('regional_name', member.regional_name)
    member.regional_position = data.get('regional_position', member.regional_position)
    member.regional_email = data.get('regional_email', member.regional_email)
    member.regional_address = data.get('regional_address', member.regional_address)
    member.regional_city = data.get('regional_city', member.regional_city)
    member.regional_state = data.get('regional_state', member.regional_state)
    member.regional_country = data.get('regional_country', member.regional_country)
    member.regional_telephone = data.get('regional_telephone', member.regional_telephone)
    member.regional_telephone2 = data.get('regional_telephone2', member.regional_telephone2)
    member.regional_fax = data.get('regional_fax', member.regional_fax)

    db.session.commit()
    return jsonify(member.as_dict()), 200



@app.route('/member-account', methods=['GET'])
@jwt_required()  
def get_member_accounts():
    members = MemberAccountAdministrator.query.all()
    return jsonify([
        {
            'id': member.id,
            'user_id': member.user_id,
            'member_name': member.member_name,
            'member_email': member.member_email,
            'agency_registration_date': member.agency_registration_date.isoformat(),
            'agency_registration_number': member.agency_registration_number,
            'hq_name': member.hq_name,
            'hq_position': member.hq_position,
            'hq_email': member.hq_email,
            'hq_address': member.hq_address,
            'hq_city': member.hq_city,
            'hq_state': member.hq_state,
            'hq_country': member.hq_country,
            'hq_telephone': member.hq_telephone,
            'hq_telephone2': member.hq_telephone2,
            'hq_fax': member.hq_fax,
            'regional_same_as_hq': member.regional_same_as_hq,
            'regional_name': member.regional_name,
            'regional_position': member.regional_position,
            'regional_email': member.regional_email,
            'regional_address': member.regional_address,
            'regional_city': member.regional_city,
            'regional_state': member.regional_state,
            'regional_country': member.regional_country,
            'regional_telephone': member.regional_telephone,
            'regional_telephone2': member.regional_telephone2,
            'regional_fax': member.regional_fax
        }
        for member in members
    ]), 200






@app.route('/member-account/<int:id>', methods=['GET'])
@jwt_required()  
def get_member_account(id):
    member = MemberAccountAdministrator.query.get_or_404(id)
    return jsonify({
        'id': member.id,
        'user_id': member.user_id,
        'member_name': member.member_name,
        'member_email': member.member_email,
        'agency_registration_date': member.agency_registration_date.isoformat(),
        'agency_registration_number': member.agency_registration_number,
        'hq_name': member.hq_name,
        'hq_position': member.hq_position,
        'hq_email': member.hq_email,
        'hq_address': member.hq_address,
        'hq_city': member.hq_city,
        'hq_state': member.hq_state,
        'hq_country': member.hq_country,
        'hq_telephone': member.hq_telephone,
        'hq_telephone2': member.hq_telephone2,
        'hq_fax': member.hq_fax,
        'regional_same_as_hq': member.regional_same_as_hq,
        'regional_name': member.regional_name,
        'regional_position': member.regional_position,
        'regional_email': member.regional_email,
        'regional_address': member.regional_address,
        'regional_city': member.regional_city,
        'regional_state': member.regional_state,
        'regional_country': member.regional_country,
        'regional_telephone': member.regional_telephone,
        'regional_telephone2': member.regional_telephone2,
        'regional_fax': member.regional_fax
    }), 200






@app.route('/agency-details', methods=['POST'])
@jwt_required()  
def create_con():
    current_user_id = get_jwt_identity()  
   
    data = request.get_json()
    
  
    required_fields = ['full_name', 'email_address', 'additional_accounts', 'email_copy']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing fields"}), 400

    
    existing_application = ConsortiumApplication.query.filter_by(email_address=data['email_address']).first()
    if existing_application:
        return jsonify({"msg": "A consortium application with this email address already exists."}), 409  

    consortium_application = ConsortiumApplication(
        full_name=data['full_name'],
        email_address=data['email_address'],
        additional_accounts=data['additional_accounts'],
        mailing_list=data.get('mailing_list', None), 
        email_copy=data['email_copy'],
        documents=data.get('documents', None),  
        user_id=current_user_id  
    )

    db.session.add(consortium_application)
    db.session.commit()

    return jsonify(consortium_application.as_dict()), 201


@app.route('/consortium_application', methods=['POST'])
@jwt_required() 
def create_consortium_application():
    current_user_id = get_jwt_identity()  

    data = request.get_json()

    full_name = data.get('full_name')
    email_address = data.get('email_address')
    additional_accounts = data.get('additional_accounts')
    mailing_list = data.get('mailing_list', '')  
    email_copy = data.get('email_copy')

    if not full_name or not email_address or not additional_accounts or not email_copy:
        return jsonify({'error': 'All fields are required unless stated otherwise.'}), 400

    try:
        additional_accounts = int(additional_accounts)
        if additional_accounts <= 0:
            raise ValueError("Requested number of additional accounts must be a positive number.")
    except ValueError:
        return jsonify({'error': 'Requested number of additional accounts must be a valid positive number.'}), 400

    new_application = ConsortiumApplication(
        full_name=full_name,
        email_address=email_address,
        additional_accounts=additional_accounts,
        mailing_list=mailing_list,
        email_copy=email_copy,
        user_id=current_user_id  
    )

    try:
        db.session.add(new_application)
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        print(f"Error occurred while saving to the database: {str(e)}")
        return jsonify({'error': 'An error occurred while saving to the database.'}), 500

    return jsonify({
        'message': (
            'Consortium Member Application successfully created! '
            'Note: This does not mean you are a member of the Minority Rights Organizations (MRO) Consortium yet. '
            'Please wait for the admin to process and validate your data. '
            'If you reached this step, you are halfway done. '
            'To complete your application, please upload the required documents: '
            'Registration Certificate, Agency Profile, Audit Report, Signed NGO Consortium Mandate, '
            'and a Signed ICRC/Red Crescent Code of Conduct.'
        ),
        'application': new_application.as_dict()
    }), 201







@app.route('/consortium_applications', methods=['GET'])
@jwt_required()  
def get_consortium_applications():
    current_user_id = get_jwt_identity()  

    applications = ConsortiumMemberApplication.query.filter_by(user_id=current_user_id).all()

    applications_list = [application.to_dict() for application in applications]

    return jsonify({'applications': applications_list}), 200



@app.route('/consortium_applications/user/<int:user_id>', methods=['GET'])
@jwt_required() 
def get_consortium_applications_by_user(user_id):
    current_user_id = get_jwt_identity() 

    if current_user_id != user_id:
        return jsonify({'error': 'You are not authorized to view this data.'}), 403

    applications = ConsortiumMemberApplication.query.filter_by(user_id=user_id).all()

    applications_list = [application.to_dict() for application in applications]

    return jsonify({'applications': applications_list}), 200










@app.route('/upload-single', methods=['POST'])
@jwt_required()
def upload_single_document():
    current_user_id = get_jwt_identity()
    if 'unique_document' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['unique_document']
    
    if file.filename == '':
        return jsonify({"error": "No selected file for uploading"}), 400

    try:
        file_path = save_file_to_directory(file)
        
        unique_document = UniqueDocument(
            user_id=current_user_id,
            document_path=file_path,
            status='Pending'  
        )

        db.session.add(unique_document)
        db.session.commit()

        return jsonify({"message": "Unique document uploaded successfully, awaiting admin approval.", "document_id": unique_document.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error uploading document, please try again."}), 500





@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    current_user_id = get_jwt_identity()
    files = request.files

    required_files = [
        'registration_certificate',
        'agency_profile',
        'audit_report',
        'ngo_consortium_mandate',
        'icrc_code_of_conduct'
    ]

    missing_files = [file_key for file_key in required_files if file_key not in files]
    if missing_files:
        return jsonify({"error": f"Missing files: {', '.join(missing_files)}"}), 400

    received_files = {}
    for file_key in required_files:
        if file_key in files and files[file_key].filename != '':
            received_files[file_key] = files[file_key]
        else:
            return jsonify({"error": f"{file_key} has no filename or is missing."}), 400

    try:
        document_upload = DocumentUpload(
            user_id=current_user_id,
            registration_certificate=save_file_to_directory(received_files['registration_certificate']),
            agency_profile=save_file_to_directory(received_files['agency_profile']),
            audit_report=save_file_to_directory(received_files['audit_report']),
            ngo_consortium_mandate=save_file_to_directory(received_files['ngo_consortium_mandate']),
            icrc_code_of_conduct=save_file_to_directory(received_files['icrc_code_of_conduct']),
            status='Pending'  
        )

        db.session.add(document_upload)
        db.session.commit()

        return jsonify({"message": "Documents submitted successfully, awaiting admin approval.", "document_id": document_upload.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "waiting for admin approval please log out and login again to check your status."}), 500

@app.route('/admin/documents', methods=['GET'])
@jwt_required()
def get_uploaded_documents():
    current_user_id = get_jwt_identity()
    
    if not is_admin(current_user_id):
        return jsonify({"error": "Access forbidden: Admins only."}), 403

    documents = DocumentUpload.query.all()
    document_list = []

    for doc in documents:
        document_list.append({
            "id": doc.id,
            "user_id": doc.user_id,
            "username": doc.user.username if doc.user else "Unknown User",
            "email": doc.user.email if doc.user else "Unknown Email",
            "registration_certificate": doc.registration_certificate,
            "agency_profile": doc.agency_profile,
            "audit_report": doc.audit_report,
            "ngo_consortium_mandate": doc.ngo_consortium_mandate,
            "icrc_code_of_conduct": doc.icrc_code_of_conduct,
            "status": doc.status,
        })

    if not document_list:
        return jsonify({"message": "No documents found."}), 404

    return jsonify(document_list), 200


def is_admin(current_user):
    """Check if the current user is an admin."""
    user = User.query.get(current_user)
    return user and user.role == 'admin'




    
@app.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_DIRECTORY, filename)

def save_file_to_directory(file):
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        file.save(file_path)
        logging.info(f"File saved to: {file_path}")  
        return filename 
    except Exception as e:
        logging.error(f"Error saving file {file.filename}: {e}")
        raise Exception("Could not save file") from e







@app.route('/admin/documents/<int:document_id>/approve', methods=['POST'])
@jwt_required()
def approve_document(document_id):
    current_user = get_jwt_identity()
    if not is_admin(current_user):
        return jsonify({"error": "Unauthorized access"}), 403

    document = DocumentUpload.query.get(document_id)
    if not document:
        return jsonify({"error": "Document not found"}), 404

    document.status = 'Approved'

    user = document.user  
    if user:
        user.is_approved = True

    db.session.commit()
    return jsonify({"message": "Document approved successfully, and user status updated."}), 200

@app.route('/admin/documents/<int:document_id>/reject', methods=['POST'])
@jwt_required()
def reject_document(document_id):
    current_user = get_jwt_identity()
    if not is_admin(current_user):
        return jsonify({"error": "Unauthorized access"}), 403

    document = DocumentUpload.query.get(document_id)
    if not document:
        return jsonify({"error": "Document not found"}), 404

    document.status = 'Rejected'

   
    user = document.user  
    if user:
        user.is_approved = False

    db.session.commit()
    return jsonify({"message": "Document rejected successfully, and user status updated."}), 200

    
    
    
@app.route('/documents', methods=['GET'])
@jwt_required()
def get_user_documents():
    current_user_id = get_jwt_identity()
    
    documents = DocumentUpload.query.filter_by(user_id=current_user_id).all()

    if not documents:
        return jsonify({"message": "No documents found for this user."}), 404

    documents_data = []
    for doc in documents:
        documents_data.append({
            "id": doc.id,
            "registration_certificate": doc.registration_certificate,
            "agency_profile": doc.agency_profile,
            "audit_report": doc.audit_report,
            "ngo_consortium_mandate": doc.ngo_consortium_mandate,
            "icrc_code_of_conduct": doc.icrc_code_of_conduct,
        })

    return jsonify({"documents": documents_data}), 200







@app.route('/reset-password', methods=['POST'])
def reset_request ():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()


    if user:
        s = URLSafeSerializer(app.secret_key)
        token = s.dumps(email, salt='password-reset-salt')

        reset_link = f'http://localhost:5173/reset-password/{token}'

        msg = Message('Password Reset Request',
                      sender= app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f'Please click the link to reset your password: {reset_link}'


        try:
            mail.send(msg)
            return make_response({
                "success": True,
                "message": "Password reset email sent. Please check your inbox."
            }, 200)
        except Exception as e:
            return make_response({
                "success": False,
                "message": "Failed to send email. Please try again."
            }, 500)
        
    return make_response({
        "success": False,
        "message": "Email not found."
    }, 404)


@app.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    s = URLSafeSerializer(app.secret_key)

    try:
        # Verify the token
        email = s.loads(token, salt='password-reset-salt')
        logging.info(f"Token valid for email: {email}")
    except Exception as e:
        logging.error(f"Token verification failed: {str(e)}")
        return make_response({
            "success": False,
            "message": "Invalid or expired token."
        }, 400)

    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return make_response({
            "success": False,
            "message": "Password cannot be empty."
        }, 400)

    user = User.query.filter_by(email=email).first()
    if user:
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        db.session.commit()

        return make_response({
            "success": True,
            "message": "Your password has been reset successfully."
        }, 200)
    
    logging.error(f"User not found for email: {email}")
    return make_response({
        "success": False,
        "message": "User not found."
    }, 404)




@app.route('/reset-password/<token>', methods=['GET'])
def verify_token(token):
    s = URLSafeSerializer(app.secret_key)

    try:
        email = s.loads(token, salt='password-reset-salt')
        logging.info(f"Token is valid. Email extracted: {email}")  
        return make_response({
            "success": True,
            "message": "Valid token. You can reset your password.",
            "email": email  
        }, 200)
    except Exception as e:
        logging.error(f"Token verification failed: {str(e)}")
        return make_response({
            "success": False,
            "message": "Invalid or expired token."
        }, 400)












api = Api(app)
api.add_resource(Users, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(VerifyToken, '/verify-token')
api.add_resource(LoginHistoryResource, '/login-history')





@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

    db.session.rollback()  
    return jsonify({"error": str(e)}), 500
    



if __name__ == '__main__':
    app.run(debug=True)
