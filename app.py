

from flask import Flask, request, jsonify, make_response, session
from models import db, ContactDetail, Agency, User ,UserAction
from config import Config

from flask import request, jsonify, session
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()


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


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            session['user_id'] = user.id  # Store user ID in session
            return make_response({
                "user": user.to_dict(),
                "access_token": access_token,
                "success": True,
                "message": "Login successful"
            }, 200)
        return make_response({"message": "Invalid credentials"}, 401)

# Resource for user logout
class Logout(Resource):
    @jwt_required()
    def post(self):
        session.pop('user_id', None)  
        return jsonify({"message": "Logout successful"}), 200

# Resource to verify JWT token
class VerifyToken(Resource):
    @jwt_required()
    def post(self):
        current_user = get_current_user()  # Use the helper to get logged-in user
        if current_user:
            return make_response({
                "user": current_user.to_dict(),
                "success": True,
                "message": "Token is valid"
            }, 200)
        return make_response({"message": "Invalid token"}, 401)
# Route to add an agency associated with the logged-in user
@app.route('/agency', methods=['POST'])
@jwt_required()  # Require authentication
def add_agency():
    current_user_id = get_jwt_identity()  # Get the current logged-in user's ID
    data = request.get_json()

    try:
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
        
        agency.user_id = current_user_id  # Associate the agency with the current logged-in user
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
            "user_id": agency.user_id  # You can include the user_id as well
        }

        return jsonify({"message": "Agency added successfully!", "agency": response_data}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get user actions associated with the logged-in user
@app.route('/user/actions', methods=['GET'])
@jwt_required()  # Require authentication
def get_user_actions():
    current_user = get_current_user()  # Get the current logged-in user
    actions = UserAction.query.filter_by(user_id=current_user.id).all()
    return jsonify([action.as_dict() for action in actions]), 200

# Route to update the agency associated with the logged-in user
@app.route('/agency/<int:agency_id>', methods=['PUT'])
@jwt_required()  # Require authentication
def update_agency(agency_id):
    current_user = get_current_user()  # Get the current logged-in user
    data = request.get_json()

    agency = Agency.query.filter_by(id=agency_id, user_id=current_user.id).first()  # Ensure agency belongs to the logged-in user
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

# Route to log user actions
@app.route('/log-action', methods=['POST'])
@jwt_required()  # Require authentication
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


api = Api(app)
api.add_resource(Users, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(VerifyToken, '/verify-token')

@app.route('/agency/<int:agency_id>', methods=['DELETE'])
@jwt_required()  
def delete_agency(agency_id):
    user_id = get_jwt_identity()  
    agency = Agency.query.filter_by(id=agency_id, user_id=user_id).first_or_404()  
    db.session.delete(agency)
    db.session.commit()
    return jsonify({"message": "Agency deleted successfully!"}), 200

@app.route('/api/contact-details', methods=['POST'])
@jwt_required()  
def save_contact_details():
    user_id = get_jwt_identity()  
    data = request.get_json()
    print("Incoming data:", data)  

    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid input"}), 400

    # Combine all contact details into a single entry
    combined_details = []

    if data.get('founders'):
        if isinstance(data['founders'], list):
            for founder in data['founders']:
                if isinstance(founder, dict):  # Check if each founder is a dictionary
                    combined_details.append({
                        'name': founder.get('name', ''),
                        'contact': founder.get('contact', ''),
                        'clan': founder.get('clan', ''),
                        'role': 'founder',
                        'user_id': user_id  # Associate contact with the user
                    })

    # Validate boardDirectors
    if data.get('boardDirectors'):
        if isinstance(data['boardDirectors'], list):
            for director in data['boardDirectors']:
                if isinstance(director, dict):  # Check if each director is a dictionary
                    combined_details.append({
                        'name': director.get('name', ''),
                        'contact': director.get('contact', ''),
                        'clan': director.get('clan', ''),
                        'role': 'board_director',
                        'user_id': user_id  # Associate contact with the user
                    })

    # Validate keyStaffs
    if data.get('keyStaffs'):
        if isinstance(data['keyStaffs'], list):
            for staff in data['keyStaffs']:
                if isinstance(staff, dict):  # Check if each staff is a dictionary
                    combined_details.append({
                        'name': staff.get('name', ''),
                        'contact': staff.get('contact', ''),
                        'clan': staff.get('clan', ''),
                        'role': 'key_staff',
                        'user_id': user_id  # Associate contact with the user
                    })

    # Save combined contact details to the database
    for detail in combined_details:
        new_contact_detail = ContactDetail(
            name=detail['name'],
            contact=detail['contact'],
            clan=detail['clan'],
            role=detail['role'],
            user_id=user_id  
        )
        db.session.add(new_contact_detail)

    db.session.commit()

    return jsonify({"message": "Contact details saved successfully!"}), 201

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
