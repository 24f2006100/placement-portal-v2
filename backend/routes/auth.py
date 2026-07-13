from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, Student, Company

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    branch = data.get("branch")
    cgpa = data.get("cgpa")
    graduation_year = data.get("graduation_year")
    phone = data.get("phone")

    if not all([full_name, email, password]):
        return jsonify({"message":"Required fields are missing"}),400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message":"Email already registered"}),409

    user = User(
        full_name=full_name,
        email=email,
        password_hash=generate_password_hash(password),
        role="student"
    )

    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        branch=branch,
        cgpa=cgpa,
        graduation_year=graduation_year,
        phone=phone
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"message":"Student registered successfully"}),201

@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    company_name = data.get("company_name")
    website = data.get("website")
    hr_name = data.get("hr_name")
    hr_email = data.get("hr_email")

    if not all([full_name, email, password, company_name]):
        return jsonify({"message":"Required fields are missing"}),400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message":"Email already registered"}),409

    user = User(
        full_name=full_name,
        email=email,
        password_hash=generate_password_hash(password),
        role="company"
    )

    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.id,
        company_name=company_name,
        website=website,
        hr_name=hr_name,
        hr_email=hr_email,
        approval_status="Pending"
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({"message":"Company registered successfully"}),201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password:
        return jsonify({"message":"Email and Password are required"}),400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message":"Invalid email, password, or role"}),401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"message":"Invalid email, password, or role"}),401
    
    if user.role == "deactivated":
        return jsonify({"message": "Your account has been deactivated"}), 403
    
    if user.role != role:
        return jsonify({"message":"Invalid email, password, or role"}),401
    
    if not user.is_active:
        return jsonify({"message":"Account has been deactivated by the administrator."}),403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role,
            "email": user.email
        }
    )

    return jsonify({
        "message":"Login Successful",
        "access_token": access_token,
        "role": user.role,
        "full_name": user.full_name,
    }),200

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    claims = get_jwt()

    return jsonify({
        "message":"Protected Route",
        "role":claims["role"],
        "email":claims["email"]
    })