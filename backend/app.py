from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from config import Config
from extensions import db,jwt
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp
from models import *
from cache_config import cache

app=Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)
jwt.init_app(app)
cache.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)

@app.route("/")
def home():
    return {"message":"Placement Portal API is Running"}


if __name__=="__main__":
    with app.app_context():
        db.create_all()

        admin=User.query.filter_by(role="admin").first()

        if not admin:
            admin=User(
                full_name="Admin",
                email="admin@portal.com",
                password_hash=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

    print(app.url_map)

    app.run(debug=True)