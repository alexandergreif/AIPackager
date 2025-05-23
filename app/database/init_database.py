"""
Database initialization script for the AIPackager application.
This script sets up the database tables and provides utility functions for database management.
"""

import os
from flask import Flask
from app.database.database_connector import init_db, db, User, Package


def create_app_for_db_init():
    """Create a minimal Flask app for database initialization."""
    app = Flask(__name__)

    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, "../../aipackager.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app


def initialize_database():
    """Initialize the database with all tables."""
    app = create_app_for_db_init()

    with app.app_context():
        init_db(app)
        print("Database initialized successfully!")
        print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")


def create_test_user():
    """Create a test user for development purposes."""
    app = create_app_for_db_init()
    init_db(app)

    with app.app_context():
        # Check if test user already exists
        existing_user = User.query.filter_by(username="testuser").first()
        if existing_user:
            print("Test user already exists!")
            return existing_user

        # Create test user
        test_user = User(
            username="testuser", email="test@example.com", password="testpassword123"
        )

        db.session.add(test_user)
        db.session.commit()

        print("Test user created successfully!")
        print(f"Username: testuser")
        print(f"Email: test@example.com")
        print(f"Password: testpassword123")

        return test_user


def drop_all_tables():
    """Drop all database tables (use with caution!)."""
    app = create_app_for_db_init()
    init_db(app)

    with app.app_context():
        db.drop_all()
        print("All tables dropped successfully!")


def reset_database():
    """Reset the database by dropping and recreating all tables."""
    app = create_app_for_db_init()
    init_db(app)

    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()

        print("Creating all tables...")
        db.create_all()

        print("Database reset successfully!")


def get_database_info():
    """Get information about the current database state."""
    app = create_app_for_db_init()
    init_db(app)

    with app.app_context():
        user_count = User.query.count()
        package_count = Package.query.count()

        print(f"Database Info:")
        print(f"- Users: {user_count}")
        print(f"- Packages: {package_count}")
        print(f"- Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

        return {
            "users": user_count,
            "packages": package_count,
            "database_uri": app.config["SQLALCHEMY_DATABASE_URI"],
        }


if __name__ == "__main__":
    """Run database initialization when script is executed directly."""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "init":
            initialize_database()
        elif command == "reset":
            reset_database()
        elif command == "info":
            get_database_info()
        elif command == "testuser":
            create_test_user()
        elif command == "drop":
            confirm = input("Are you sure you want to drop all tables? (yes/no): ")
            if confirm.lower() == "yes":
                drop_all_tables()
            else:
                print("Operation cancelled.")
        else:
            print("Available commands:")
            print("  init     - Initialize database tables")
            print("  reset    - Drop and recreate all tables")
            print("  info     - Show database information")
            print("  testuser - Create a test user")
            print("  drop     - Drop all tables (with confirmation)")
    else:
        # Default action: initialize database
        initialize_database()
