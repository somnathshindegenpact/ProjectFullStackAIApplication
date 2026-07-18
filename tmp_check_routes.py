import app
flask_app = app.create_app()
print(flask_app.url_map)
