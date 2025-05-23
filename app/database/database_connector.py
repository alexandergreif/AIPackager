from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and user management."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    packages = db.relationship(
        "Package", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, username, email, password):
        """Initialize a new user with hashed password."""
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Return the user ID as a string (required by Flask-Login)."""
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"


class Package(db.Model):
    """Package model for tracking uploaded packages and their processing status."""

    __tablename__ = "packages"

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    app_name = db.Column(db.String(200), nullable=False)
    vendor = db.Column(db.String(200), nullable=True)
    version = db.Column(db.String(50), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    script_created = db.Column(db.Boolean, default=False, nullable=False)
    testing_passed = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.String(50), default="uploaded", nullable=False)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Additional fields for script content and testing results
    script_content = db.Column(db.Text, nullable=True)
    testing_results = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)

    def __init__(
        self,
        package_id,
        app_name,
        filename,
        file_path,
        user_id,
        vendor=None,
        version=None,
        instructions=None,
    ):
        """Initialize a new package record."""
        self.package_id = package_id
        self.app_name = app_name
        self.vendor = vendor
        self.version = version
        self.filename = filename
        self.file_path = file_path
        self.user_id = user_id
        self.instructions = instructions

    def update_status(self, status):
        """Update the package status."""
        self.status = status
        db.session.commit()

    def mark_script_created(self, script_content=None):
        """Mark the package as having a script created."""
        self.script_created = True
        if script_content:
            self.script_content = script_content
        self.status = "script_generated"
        db.session.commit()

    def mark_testing_passed(self, testing_results=None):
        """Mark the package as having passed testing."""
        self.testing_passed = True
        if testing_results:
            self.testing_results = testing_results
        self.status = "tested"
        db.session.commit()

    def __repr__(self):
        return f"<Package {self.package_id}: {self.app_name}>"


def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)

    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")


def get_db():
    """Get the database instance."""
    return db
