

from flask import Flask, request, jsonify, make_response, session
from models import db, Founder, Agency, User ,UserAction ,BoardDirector,KeyStaff,Consortium ,MemberAccountAdministrator,ConsortiumApplication
from config import Config
from flask_login import  login_required,  current_user,LoginManager
from flask import request, jsonify, session
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime,timedelta
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
login_manager = LoginManager(app)  
login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['SESSION_COOKIE_HTTPONLY'] = True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


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
    


#   



class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            session['user_id'] = user.id 
            return make_response({
                "user": user.to_dict(),
                "access_token": access_token,
                "success": True,
                "message": "Login successful"
            }, 200)
        return make_response({"message": "Invalid credentials"}, 401)

# 


class Logout(Resource):
    @jwt_required()
    def post(self):
        session.pop('user_id', None)  
        return jsonify({"message": "Logout successful"}), 200

# Resource to verify JWT token
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
@jwt_required()  # Require authentication
def add_agency():
    # Get the current logged-in user's ID from the JWT token
    current_user_id = get_jwt_identity()  
    # Optionally log the user ID (can be removed in production)
    print(f"User ID: {current_user_id}")

    # Get JSON data from the request
    data = request.get_json()
    
    try:
        # Create a new Agency instance with provided data
        agency = Agency(
            full_name=data['full_name'],
            acronym=data.get('acronym'),  # optional
            description=data['description'],
            mission_statement=data['mission_statement'],
            website=data['website'],
            is_ngo=data['is_ngo'],
            years_operational=data['years_operational'],
            reason_for_joining=data['reason_for_joining'],
            willing_to_participate=data['willing_to_participate'],
            commitment_to_principles=data['commitment_to_principles'],
        )
        
        # Associate the agency with the current logged-in user
        agency.user_id = current_user_id  
        # Add the agency to the session and commit to the database
        db.session.add(agency)
        db.session.commit()

        # Prepare the response data
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
            "user_id": agency.user_id  # Storing the user_id in the response
        }

        return jsonify({"message": "Agency added successfully!", "agency": response_data}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
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

@app.route('/agency/<int:agency_id>', methods=['PUT'])
@jwt_required()
def update_agency(agency_id):
    current_user = get_current_user() 
    data = request.get_json()

    agency = Agency.query.filter_by(id=agency_id, user_id=current_user.id).first()  
    if not agency:
        return jsonify({"message": "Agency not found or not authorized"}), 404

    try:
        agency.full_name = data.get('full_name', agency.full_name)
        agency.acronym = data.get('acronym', agency.acronym)
        agency.description = data.get('description', agency.description)
        agency.mission_statement = data.get('mission_statement', agency.mission_statement)
        agency.website = data.get('website', agency.website)
        agency.is_ngo = data.get('is_ngo', agency.is_ngo)
        agency.years_operational = data.get('years_operational', agency.years_operational)
        agency.reason_for_joining = data.get('reason_for_joining', agency.reason_for_joining)
        agency.willing_to_participate = data.get('willing_to_participate', agency.willing_to_participate)
        agency.commitment_to_principles = data.get('commitment_to_principles', agency.commitment_to_principles)

        db.session.commit()

        return jsonify({"message": "Agency updated successfully!"}), 200
    except Exception as e:
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
@jwt_required()  # Change this to JWT-based authentication
def create_founder():
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    print(f"User ID: {current_user_id}")  # Debug
    
    data = request.json
    new_founder = Founder(
        name=data['name'],
        contact=data['contact'],
        clan=data['clan'],
        user_id=current_user_id  # Associate founder with the current logged-in user
    )
    db.session.add(new_founder)
    db.session.commit()

    user_action = UserAction(user_id=current_user_id, action="Created a founder")
    db.session.add(user_action)
    db.session.commit()

    return jsonify(new_founder.as_dict()), 201







@app.route('/founders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()  # Ensure that a valid JWT token is required to access this route
def handle_founder(id):
    # Get the current user ID from the JWT token
    current_user_id = get_jwt_identity()
    print(f"User ID: {current_user_id}")

    founder = Founder.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(founder.as_dict()), 200

    elif request.method == 'PUT':
        data = request.json
        founder.name = data.get('name', founder.name)
        founder.contact = data.get('contact', founder.contact)
        founder.clan = data.get('clan', founder.clan)
        founder.user_id = current_user_id  # Optionally associate the founder with the current user

        db.session.commit()
        return jsonify(founder.as_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(founder)
        db.session.commit()
        return jsonify({"message": "Founder deleted"}), 200








@app.route('/board-directors', methods=['GET', 'POST'])
@jwt_required()  # Ensure the user is authenticated before accessing this route
def handle_board_directors():
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    print(f"User ID: {current_user_id}")  # Log the current user ID for debugging purposes

    if current_user_id is None:
        return jsonify({"msg": "User ID not found in token."}), 401  # Unauthorized if user ID is None

    if request.method == 'POST':
        data = request.json
        
        new_board_director = BoardDirector(
            name=data.get('name'),
            contact=data.get('contact'),
            clan=data.get('clan'),
            user_id=current_user_id  # Set the user_id from the JWT
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


# @app.route('/key-staff', methods=['GET', 'POST'])
# @jwt_required()  # Protect this route with JWT authentication
# def handle_key_staff():
#     current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
#     print(f"User ID: {current_user_id}")  # Log the current user ID for debugging purposes

#     if current_user_id is None:
#         return jsonify({"msg": "User ID not found in token."}), 401  # Unauthorized if user ID is None

#     if request.method == 'POST':
#         data = request.json
#         new_staff = KeyStaff(
#             name=data.get('name'),
#             contact=data.get('contact'),
#             clan=data.get('clan'),
#             user_id=current_user_id  # Use the current user ID from the token
#         )
#         db.session.add(new_staff)
#         db.session.commit()
#         return jsonify(new_staff.as_dict()), 201

#     elif request.method == 'GET':
#         staff = KeyStaff.query.all()
#         return jsonify([s.as_dict() for s in staff]), 200

@app.route('/key-staff', methods=['GET', 'POST'])
@jwt_required()
def handle_key_staff():
    current_user_id = get_jwt_identity()
    print(f"User ID: {current_user_id}")

    if request.method == 'POST':
        data = request.json
        
        # Validate input data
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
            db.session.rollback()  # Rollback on error
            return jsonify({"msg": str(e)}), 500  # Return server error


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









@app.route('/consortium', methods=['POST'])
@jwt_required()  # Protect this route with JWT
def create_consortium():
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    print(f"User ID: {current_user_id}")

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
        user_id=current_user_id  # Associate with the current user
    )
    
    db.session.add(new_consortium)
    db.session.commit()
    
    return jsonify(new_consortium.as_dict()), 201

@app.route('/consortium', methods=['GET'])
@jwt_required()  # Protect this route with JWT
def get_consortia():
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    print(f"User ID: {current_user_id}")

    consortia = Consortium.query.filter_by(user_id=current_user_id).all()
    return jsonify([consortium.as_dict() for consortium in consortia]), 200





# @app.route('/member-account', methods=['POST'])
# def create_member_account():
#     data = request.json
#     try:
#         new_member = MemberAccountAdministrator(
#             member_name=data['member_name'],
#             member_email=data['member_email'],
#             agency_registration_date=datetime.fromisoformat(data['agency_registration_date']),
#             agency_registration_number=data['agency_registration_number'],
#             hq_name=data['hq_name'],
#             hq_position=data['hq_position'],
#             hq_email=data['hq_email'],
#             hq_address=data['hq_address'],
#             hq_city=data['hq_city'],
#             hq_state=data['hq_state'],
#             hq_country=data['hq_country'],
#             hq_zip_code=data['hq_zip_code'],
#             user_id=data['user_id']
#         )
#         db.session.add(new_member)
#         db.session.commit()
#         return jsonify(new_member.as_dict()), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# # API route to get all member account administrators
# @app.route('/member-account', methods=['GET'])
# def get_member_accounts():
#     members = MemberAccountAdministrator.query.all()
#     return jsonify([member.as_dict() for member in members]), 200

# # API route to get a member account by ID
# @app.route('/member-account/<int:id>', methods=['GET'])
# def get_member_account(id):
#     member = MemberAccountAdministrator.query.get_or_404(id)
#     return jsonify(member.as_dict()), 200

# # API route to update a member account
# @app.route('/member-account/<int:id>', methods=['PUT'])
# def update_member_account(id):
#     data = request.json
#     member = MemberAccountAdministrator.query.get_or_404(id)

#     member.member_name = data.get('member_name', member.member_name)
#     member.member_email = data.get('member_email', member.member_email)
#     member.agency_registration_date = datetime.fromisoformat(data.get('agency_registration_date', member.agency_registration_date.isoformat()))
#     member.agency_registration_number = data.get('agency_registration_number', member.agency_registration_number)
#     member.hq_name = data.get('hq_name', member.hq_name)
#     member.hq_position = data.get('hq_position', member.hq_position)
#     member.hq_email = data.get('hq_email', member.hq_email)
#     member.hq_address = data.get('hq_address', member.hq_address)
#     member.hq_city = data.get('hq_city', member.hq_city)
#     member.hq_state = data.get('hq_state', member.hq_state)
#     member.hq_country = data.get('hq_country', member.hq_country)
#     member.hq_zip_code = data.get('hq_zip_code', member.hq_zip_code)

#     db.session.commit()
#     return jsonify(member.as_dict()), 200

# # API route to delete a member account
# @app.route('/member-account/<int:id>', methods=['DELETE'])
# def delete_member_account(id):
#     member = MemberAccountAdministrator.query.get_or_404(id)
#     db.session.delete(member)
#     db.session.commit()
#     return jsonify({'message': 'Member account deleted successfully.'}), 200











@app.route('/member-account', methods=['POST'])
@jwt_required()  # Protect this route with JWT
def create_member_account():
    data = request.json
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    
    try:
        new_member = MemberAccountAdministrator(
            member_name=data['member_name'],
            member_email=data['member_email'],
            agency_registration_date=datetime.fromisoformat(data['agency_registration_date']),
            agency_registration_number=data.get('agency_registration_number'),  # Use .get() for optional fields
            hq_name=data['hq_name'],
            hq_position=data['hq_position'],
            hq_email=data['hq_email'],
            hq_address=data['hq_address'],
            hq_city=data['hq_city'],
            hq_state=data['hq_state'],
            hq_country=data['hq_country'],
            hq_telephone=data['hq_telephone'],
            hq_telephone2=data.get('hq_telephone2'),  # Optional
            hq_fax=data.get('hq_fax'),  # Optional
            regional_same_as_hq=data.get('regional_same_as_hq', False),  # Default to False if not provided
            regional_name=data.get('regional_name'),  # Optional
            regional_position=data.get('regional_position'),  # Optional
            regional_email=data.get('regional_email'),  # Optional
            regional_address=data.get('regional_address'),  # Optional
            regional_city=data.get('regional_city'),  # Optional
            regional_state=data.get('regional_state'),  # Optional
            regional_country=data.get('regional_country'),  # Optional
            regional_telephone=data.get('regional_telephone'),  # Optional
            regional_telephone2=data.get('regional_telephone2'),  # Optional
            regional_fax=data.get('regional_fax'),  # Optional
            user_id=current_user_id  # Use the user ID from the JWT token
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify(new_member.as_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/member-account/<int:id>', methods=['PUT'])
@jwt_required()  # Protect this route with JWT
def update_member_account(id):
    data = request.json
    member = MemberAccountAdministrator.query.get_or_404(id)
    
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    
    # Additional check: Only allow updates if the user is the owner
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



# API route to get all member account administrators
@app.route('/member-account', methods=['GET'])
@jwt_required()  # Protect this route with JWT
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

# API route to get a member account by ID
@app.route('/member-account/<int:id>', methods=['GET'])
@jwt_required()  # Protect this route with JWT
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
@jwt_required()  # Protect this route with JWT
def create_con():
    current_user_id = get_jwt_identity()  # Get the current user's ID from the JWT
    
    # Get data from the request
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['full_name', 'email_address', 'additional_accounts', 'email_copy']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing fields"}), 400

    # Check for existing applications with the same email address
    existing_application = ConsortiumApplication.query.filter_by(email_address=data['email_address']).first()
    if existing_application:
        return jsonify({"msg": "A consortium application with this email address already exists."}), 409  # Conflict

    # Create a new consortium application
    consortium_application = ConsortiumApplication(
        full_name=data['full_name'],
        email_address=data['email_address'],
        additional_accounts=data['additional_accounts'],
        mailing_list=data.get('mailing_list', None),  # Optional field
        email_copy=data['email_copy'],
        documents=data.get('documents', None),  # Optional field
        user_id=current_user_id  # Associate the application with the current user
    )

    # Add the application to the session and commit
    db.session.add(consortium_application)
    db.session.commit()

    return jsonify(consortium_application.as_dict()), 201












api = Api(app)
api.add_resource(Users, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(VerifyToken, '/verify-token')





@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
