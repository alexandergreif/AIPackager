from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    flash,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from app.orchestrator import run_script_generation
from app.utils.installer_utils import get_installer_type
from app.agents.script_agent import generate_psadt_script
from app.database.database_connector import db, init_db, User, Package
import uuid, os, logging, re

from dotenv import load_dotenv
import os
import logging

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# --- Logging Config ---
log_path = os.path.join(os.getcwd(), "logs", "aipackager.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)

# App configuration
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aipackager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("logs", exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize database and login manager
init_db(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"


def validate_username(username):
    """Validate username format."""
    if len(username) < 3 or len(username) > 80:
        return False, "Username must be between 3 and 80 characters"
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, "Username is valid"


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration route."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validation
        errors = []

        # Check if all fields are provided
        if not username:
            errors.append("Username is required")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if not confirm_password:
            errors.append("Password confirmation is required")

        # Validate username
        if username:
            is_valid, message = validate_username(username)
            if not is_valid:
                errors.append(message)

        # Validate password
        if password:
            is_valid, message = validate_password(password)
            if not is_valid:
                errors.append(message)

        # Check password confirmation
        if password and confirm_password and password != confirm_password:
            errors.append("Passwords do not match")

        # Check if username already exists
        if username and User.query.filter_by(username=username).first():
            errors.append("Username already exists")

        # Check if email already exists
        if email and User.query.filter_by(email=email).first():
            errors.append("Email already registered")

        # If there are errors, show them
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("register.html")

        # Create new user
        try:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! You can now log in.", "success")
            logging.info(f"New user registered: {username}")
            return redirect(url_for("login"))

        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration. Please try again.", "error")
            logging.error(f"Registration error: {str(e)}")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
def upload():
    # Add functionality for users to provide instructions to the model, including installer details, silent switches, config files, and custom registry keys for the organization.
    # This includes handling installer details, silent switches, and any associated config files.
    # Additionally, incorporate custom registry keys specific to the organization.
    # Extract and process the application name, version, and installer type.
    # Retrieve the installer type using the function from installer_utils.py.
    # PackageIDs are four-digit unique identifiers (e.g., 0001) for tracking packaging processes.
    # because we will handle the whole packaging process flow with it.

    # Handle file uploads and gather software information using get_installer_type.
    # Consider using a function to extract installation switches if needed.
    # Create a package request through the package request handler.

    # Add functionality for users to provide instructions
    user_instructions = request.form.get("instructions", "")  # Get from form
    installer_file = request.files.get("file")  # Get uploaded file
    if installer_file:
        installer_type = get_installer_type(installer_file.filename)
        package_id = str(uuid.uuid4())  # Generate unique ID
        # Save file and process
        installer_file.save(
            os.path.join(app.config["UPLOAD_FOLDER"], installer_file.filename)
        )
        # Run script generation
        script_content = run_script_generation(user_instructions, installer_type)
        # Save or store script_content with packageID
        return redirect(url_for("result", packageID=package_id))
    return render_template("upload.html")


@app.route("/result/<packageID>")
def result(packageID):
    # Fetch actual content based on packageID
    # For now, use a placeholder; in T1.9 and T1.10, this will be updated
    # Fetch actual content based on packageID from the orchestrator
    content = run_script_generation(packageID)  # Use the function to get real script
    return render_template("result.html", script=content, id=packageID)


@app.route("/download/<packageID>")
def download(packageID):
    # Generate or fetch the actual file path based on packageID
    script_path = os.path.join("downloads", f"{packageID}_script.ps1")
    return send_from_directory(
        os.path.dirname(script_path), os.path.basename(script_path), as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
