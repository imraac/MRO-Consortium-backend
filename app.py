# from flask import Flask, request, jsonify
# from models import db, Agency
# from config import Config
# from flask_cors import CORS
# from flask_migrate import Migrate 
# from flask_sqlalchemy import SQLAlchemy
# app = Flask(__name__)
# CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})  # Allow all origins
#  # Allow all routes
#  # Allow all routes

# app.config.from_object(Config)

# # Initialize the database
# db.init_app(app)

# migrate = Migrate(app, db)
# # Create tables at the application startup
# with app.app_context():
#     db.create_all()

# # Route to add a new agency
# @app.route('/agency', methods=['POST'])
# def add_agency():
#     data = request.get_json()

#     try:
#         agency = Agency(
#             full_name=data['full_name'],
#             acronym=data.get('acronym'),  # optional
#             description=data['description'],
#             mission_statement=data['mission_statement'],
#             website=data['website'],
#             is_ngo=data['is_ngo'],
#             years_operational=data['years_operational'],
#             reason_for_joining=data['reason_for_joining'],
#             willing_to_participate=data['willing_to_participate'],
#             commitment_to_principles=data['commitment_to_principles']
#         )
#         db.session.add(agency)
#         db.session.commit()

#         return jsonify({"message": "Agency added successfully!"}), 201
#     except KeyError as e:
#         return jsonify({"error": f"Missing field: {str(e)}"}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Route to get all agencies
# @app.route('/agencies', methods=['GET'])
# def get_agencies():
#     agencies = Agency.query.all()
#     return jsonify([agency.as_dict() for agency in agencies]), 200

# # Route to update an agency
# @app.route('/agency/<int:agency_id>', methods=['PUT'])
# def update_agency(agency_id):
#     agency = Agency.query.get_or_404(agency_id)
#     data = request.get_json()

#     agency.full_name = data.get('full_name', agency.full_name)
#     agency.acronym = data.get('acronym', agency.acronym)
#     agency.description = data.get('description', agency.description)
#     agency.mission_statement = data.get('mission_statement', agency.mission_statement)
#     agency.website = data.get('website', agency.website)
#     agency.is_ngo = data.get('is_ngo', agency.is_ngo)
#     agency.years_operational = data.get('years_operational', agency.years_operational)
#     agency.reason_for_joining = data.get('reason_for_joining', agency.reason_for_joining)
#     agency.willing_to_participate = data.get('willing_to_participate', agency.willing_to_participate)
#     agency.commitment_to_principles = data.get('commitment_to_principles', agency.commitment_to_principles)

#     db.session.commit()
#     return jsonify({"message": "Agency updated successfully!"}), 200

# # Route to delete an agency
# @app.route('/agency/<int:agency_id>', methods=['DELETE'])
# def delete_agency(agency_id):
#     agency = Agency.query.get_or_404(agency_id)
#     db.session.delete(agency)
#     db.session.commit()
#     return jsonify({"message": "Agency deleted successfully!"}), 200



# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from models import db, ContactDetail, Agency, Consortium, MemberAccountAdministrator # Ensure ContactDetail and Agency are imported
from config import Config
from flask_cors import CORS
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})  # Allow all origins

app.config.from_object(Config)

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Create tables at the application startup
with app.app_context():
    db.create_all()

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

# Route to get all agencies
@app.route('/agencies', methods=['GET'])
def get_agencies():
    agencies = Agency.query.all()
    return jsonify([agency.as_dict() for agency in agencies]), 200

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

# Route to delete an agency
@app.route('/agency/<int:agency_id>', methods=['DELETE'])
def delete_agency(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    db.session.delete(agency)
    db.session.commit()
    return jsonify({"message": "Agency deleted successfully!"}), 200

# Route to save contact details
@app.route('/api/contact-details', methods=['POST'])
def save_contact_details():
    data = request.get_json()
    print("Incoming data:", data)  # Log the incoming data

    # Validate input
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid input"}), 400

    # Combine all contact details into a single entry
    combined_details = []

    # Validate founders
    if data.get('founders'):
        if isinstance(data['founders'], list):
            for founder in data['founders']:
                if isinstance(founder, dict):  # Check if each founder is a dictionary
                    combined_details.append({
                        'name': founder.get('name', ''),
                        'contact': founder.get('contact', ''),
                        'clan': founder.get('clan', ''),
                        'role': 'founder'
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
                        'role': 'board_director'
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
                        'role': 'key_staff'
                    })

    # Save combined details in one go
    for detail in combined_details:
        new_contact_detail = ContactDetail(
            name=detail['name'],
            contact=detail['contact'],
            clan=detail['clan'],
            role=detail['role']
        )
        db.session.add(new_contact_detail)

    try:
        db.session.commit()
        return jsonify({"message": "Contact details saved successfully!"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback if there's an error
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/consortium', methods=['POST'])
def save_consortium():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_consortium = Consortium(
        active_year=data.get('activeYear'),
        partner_ngos=data.get('partnerNGOs'),
        international_staff=data.get('internationalStaff'),
        national_staff=data.get('nationalStaff'),
        program_plans=data.get('programPlans'),
        main_donors=data.get('mainDonors'),
        annual_budget=data.get('annualBudget'),
        membership_type=data.get('membershipType')
    )

    try:
        db.session.add(new_consortium)  
        db.session.commit()  
        return jsonify({"message": "Data saved successfully!", "data": data}), 201
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 400
    from flask import request, jsonify

@app.route('/api/member', methods=['POST'])
def create_member():
    data = request.json

    agency_registration_date_str = data.get('agency_registration_date')  

    try:
        agency_registration_date = datetime.strptime(agency_registration_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError) as e:
        return jsonify({"error": "Invalid date format, should be YYYY-MM-DD"}), 400

    new_member = MemberAccountAdministrator(
        agency_registration_date=agency_registration_date,
        agency_registration_number=data.get('agency_registration_number'),
        hq_name=data['hq_name'],
        hq_position=data['hq_position'],
        hq_email=data['hq_email'],
        hq_address=data['hq_address'],
        hq_city=data['hq_city'],
        hq_state=data['hq_state'],
        hq_country=data['hq_country'],
        hq_telephone=data['hq_telephone'],
        hq_fax=data.get('hq_fax'),
        regional_name=data.get('regional_name'),
        regional_position=data.get('regional_position'),
        regional_email=data.get('regional_email'),
        regional_address=data.get('regional_address'),
        regional_city=data.get('regional_city'),
        regional_state=data.get('regional_state'),
        regional_country=data.get('regional_country'),
        regional_telephone=data.get('regional_telephone'),
        regional_fax=data.get('regional_fax')
    )

    try:
        db.session.add(new_member)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Member created successfully", "id": new_member.id}), 201


if __name__ == '__main__':
    app.run(debug=True)
