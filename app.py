from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from models import db, User, Agency, BoardDirector, KeyStaff, Founder, ContactDetail  # Import all necessary models
from config import Config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/": {"origins": ""}})  # Allow all origins
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this to a more secure key
app.config.from_object(Config)

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Create tables at the application startup
with app.app_context():
    db.create_all()

# User Resource for Authentication
class Users(Resource):
    def post(self):
        # User Registration
        data = request.get_json()
        email = User.query.filter_by(email=data.get('email')).first()
        if email:
            return make_response({"message": "Email already taken"}, 422)

        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=bcrypt.generate_password_hash(data.get("password")).decode('utf-8'),
            role=data.get("role", "user")
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
        # User Login
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return make_response({
                "user": user.to_dict(),
                "access_token": access_token,
                "success": True,
                "message": "Login successful"
            }, 200)
        return make_response({"message": "Invalid credentials"}, 401)


class VerifyToken(Resource):
    @jwt_required()
    def post(self):
        # Verify JWT Token
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            return make_response({
                "user": user.to_dict(),
                "success": True,
                "message": "Token is valid"
            }, 200)
        return make_response({"message": "Invalid token"}, 401)

# Add the Resources to the API
api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(VerifyToken, '/verify-token')

# Route to add a new agency
@app.route('/agency', methods=['POST'])
def add_agency():
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
            commitment_to_principles=data['commitment_to_principles']
        )
        db.session.add(agency)
        db.session.commit()

        return jsonify({"message": "Agency added successfully!"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Additional agency routes go here...



# Route to update an agency
@app.route('/agency/<int:agency_id>', methods=['PUT'])
def update_agency(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    data = request.get_json()

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

# Route to save contact details, including founders, board directors, and key staff
@app.route('/api/contact-details', methods=['POST'])
def save_contact_details():
    data = request.get_json()
    print("Incoming data:", data)  # Log the incoming data

    # Validate input
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid input"}), 400

    # Process and save founders
    if data.get('founders'):
        for founder_data in data['founders']:
            if isinstance(founder_data, dict):  # Ensure it's a dictionary
                founder = Founder(
                    name=founder_data.get('name', ''),
                    contact=founder_data.get('contact', ''),
                    clan=founder_data.get('clan', '')
                )
                db.session.add(founder)

    # Process and save board directors
    if data.get('boardDirectors'):
        for director_data in data['boardDirectors']:
            if isinstance(director_data, dict):  # Ensure it's a dictionary
                board_director = BoardDirector(
                    name=director_data.get('name', ''),
                    contact=director_data.get('contact', ''),
                    clan=director_data.get('clan', '')
                )
                db.session.add(board_director)

    # Process and save key staff
    if data.get('keyStaffs'):
        for staff_data in data['keyStaffs']:
            if isinstance(staff_data, dict):  # Ensure it's a dictionary
                key_staff = KeyStaff(
                    name=staff_data.get('name', ''),
                    contact=staff_data.get('contact', ''),
                    clan=staff_data.get('clan', '')
                )
                db.session.add(key_staff)

    try:
        db.session.commit()
        return jsonify({"message": "Contact details saved successfully!"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback if there's an error
        return jsonify({"error": str(e)}), 500

# Route to get all contact details (founders, board directors, key staff)
@app.route('/api/contact-details', methods=['GET'])
def get_contact_details():
    founders = Founder.query.all()
    board_directors = BoardDirector.query.all()
    key_staffs = KeyStaff.query.all()

    return jsonify({
        'founders': [founder.as_dict() for founder in founders],
        'boardDirectors': [director.as_dict() for director in board_directors],
        'keyStaffs': [staff.as_dict() for staff in key_staffs]
    }), 200


if __name__ == '_main_':
    app.run(debug=True)