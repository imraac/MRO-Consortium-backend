# - Minority Rights Organizations (MRO) Consortium



This application provides a RESTful API to handle user registration, login, agency management, document uploads, consortium membership applications ,agency details , admin and member management dashboards within an NGO consortium environment.

# Table of Contents
Project Setup
Database Models
User
Agency
LoginHistory
UserAction
Founder
BoardDirector
KeyStaff
Consortium
MemberAccountAdministrator
ConsortiumApplication
ConsortiumMemberApplication
DocumentUpload
Endpoints Overview
Probable Route Methods
Project Setup
Install Requirements: pip install -r requirements.txt
Initialize Database: Run database migrations to set up all tables.
Run the Application: Use flask run to start the server.
Database Models
User
Manages user details, login tracking, and roles. Fields include username, email, password, role, is_approved, and agency_id.

Agency
Stores information about agencies, including name, description, mission, and NGO status.

LoginHistory
Logs user login and logout times, connected to a User entry.

UserAction
Records various actions performed by users in the application.

Founder, BoardDirector, KeyStaff
These models store details about founders, board members, and key staff associated with users, capturing their names, contact info, and clan.

Consortium
Holds data about each consortium, such as partner NGOs, international staff, national staff, program plans, and annual budget.

MemberAccountAdministrator
Captures details about member account administrators, including headquarter information and regional contact data.

ConsortiumApplication and ConsortiumMemberApplication
Handles applications for consortium memberships, capturing names, email addresses, and mailing lists.

DocumentUpload
Manages document submissions, including the registration certificate, audit report, and status of each document upload.

Endpoints Overview
This section provides a high-level overview of probable endpoints for each feature. HTTP methods used here are assumptions based on typical CRUD operations.

Endpoint	HTTP Method	Description
/register	POST	Registers a new user
/login	POST	Authenticates a user and logs login time
/logout	POST	Logs out a user and records logout time
/users/<int:user_id>	GET	Fetches user details
/users/<int:user_id>	PUT	Updates user information
/users/<int:user_id>	DELETE	Deletes a user account
/agencies	POST	Creates a new agency
/agencies/<int:agency_id>	GET	Fetches agency information
/agencies/<int:agency_id>	PUT	Updates agency details
/login-history	GET	Retrieves login history for a user
/user-actions	GET	Fetches recorded actions of users
/founders	POST	Adds a new founder
/founders/<int:founder_id>	GET	Retrieves founder details
/board-directors	POST	Adds a new board director
/key-staff	POST	Adds a key staff member
/consortiums	POST	Creates a new consortium
/member-account-admins	POST	Adds a member account admin
/consortium-applications	POST	Submits a consortium application
/document-uploads	POST	Uploads required documents for verification
/document-uploads/status	PUT	Updates document approval status
