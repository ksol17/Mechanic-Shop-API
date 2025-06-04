from app import create_app
from app.models import db   

app = create_app("DevelopmentConfig")


with app.app_context():
    db.drop_all()  # Drop all tables if they exist

 


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


