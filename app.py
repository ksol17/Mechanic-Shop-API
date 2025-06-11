from app import create_app, db



app = create_app()




if __name__ == "__main__":
    with app.app_context():   # Ensures the app is correctly bound to Flask-SQLAlchemy
        db.create_all()
    app.run(debug=True)

for rule in app.url_map.iter_rules():
    print(rule)