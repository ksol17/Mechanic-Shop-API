from app import create_app, db



app = create_app()




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        for rule in app.url_map.iter_rules():
            print(rule)
    app.run(debug=True)