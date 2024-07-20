# run.py
from app import create_app, db
from app.models import Employee

app = create_app()

def setup_database():
    with app.app_context():
        db.create_all()
        print("Database setup complete.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'setup_db':
        setup_database()
    else:
        app.run(debug=True)
