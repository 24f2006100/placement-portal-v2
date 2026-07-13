from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import *
from datetime import datetime
from extensions import db
import os

company_bp = Blueprint("company", __name__)

@company_bp.route("/company/dashboard", methods=["GET"])
@jwt_required()
def company_dashboard():

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message":"Company not found"}),404

    if company.approval_status == "Pending":
        return jsonify({
            "status":"Pending",
            "message":"Your company registration is awaiting admin approval."
        }),200

    if company.approval_status == "Rejected":
        return jsonify({
            "status":"Rejected",
            "message":"Your company registration has been rejected."
        }),200

    return jsonify({
        "status":"Approved",
        "company_name":company.company_name,
        "total_drives":PlacementDrive.query.filter_by(company_id=company.id).count(),
        "approved_drives":PlacementDrive.query.filter_by(
            company_id=company.id,
            status="Approved"
        ).count(),
        "pending_drives":PlacementDrive.query.filter_by(
            company_id=company.id,
            status="Pending"
        ).count()
    }),200

@company_bp.route("/company/create-drive", methods=["POST"])
@jwt_required()
def create_drive():

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message":"Company not found"}),404

    if company.approval_status != "Approved":
        return jsonify({"message":"Company is not approved"}),403

    data = request.get_json()

    drive = PlacementDrive(
        company_id=company.id,
        title=data["title"],
        description=data["description"],
        salary_package=data["salary_package"],
        location=data["location"],
        branch_required=data["branch_required"],
        cgpa_required=data["cgpa_required"],
        deadline=datetime.strptime(data["deadline"], "%Y-%m-%d").date(),
        status="Pending"
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({
        "message":"Placement Drive Created Successfully"
    }),201

@company_bp.route("/company/drive/<int:id>", methods=["PUT"])
@jwt_required()
def edit_drive(id):

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    drive = PlacementDrive.query.filter_by(
        id=id,
        company_id=company.id
    ).first()

    if not drive:
        return jsonify({"message":"Drive not found"}),404

    data = request.get_json()

    drive.title = data.get("title", drive.title)
    drive.description = data.get("description", drive.description)
    drive.salary_package = data.get("salary_package", drive.salary_package)
    drive.location = data.get("location", drive.location)
    drive.branch_required = data.get("branch_required", drive.branch_required)
    drive.cgpa_required = data.get("cgpa_required", drive.cgpa_required)

    if data.get("deadline"):
        drive.deadline = datetime.strptime(
            data["deadline"],
            "%Y-%m-%d"
        ).date()

    db.session.commit()

    return jsonify({
        "message":"Drive Updated Successfully"
    }),200

@company_bp.route("/company/drive/<int:id>/close", methods=["PUT"])
@jwt_required()
def close_drive(id):

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message":"Company not found"}),404

    drive = PlacementDrive.query.filter_by(
        id=id,
        company_id=company.id
    ).first()

    if not drive:
        return jsonify({"message":"Drive not found"}),404

    drive.status = "Closed"

    db.session.commit()

    return jsonify({"message":"Drive Closed Successfully"}),200

@company_bp.route("/company/drive/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_drive(id):

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    drive = PlacementDrive.query.filter_by(
        id=id,
        company_id=company.id
    ).first()

    if not drive:
        return jsonify({"message":"Drive not found"}),404

    db.session.delete(drive)
    db.session.commit()

    return jsonify({"message":"Drive Deleted Successfully"}),200

@company_bp.route("/company/drive/<int:id>/open", methods=["PUT"])
@jwt_required()
def open_drive(id):

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    drive = PlacementDrive.query.filter_by(
        id=id,
        company_id=company.id
    ).first()

    if not drive:
        return jsonify({"message":"Drive not found"}),404

    drive.status = "Approved"

    db.session.commit()

    return jsonify({"message":"Drive Reopened"}),200

@company_bp.route("/company/drives", methods=["GET"])
@jwt_required()
def get_company_drives():

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message":"Company not found"}),404

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    drive_list = []

    for drive in drives:

        drive_list.append({

            "id": drive.id,
            "title": drive.title,
            "location": drive.location,
            "salary_package": drive.salary_package,
            "branch_required": drive.branch_required,
            "cgpa_required": drive.cgpa_required,
            "deadline": drive.deadline.strftime("%Y-%m-%d"),
            "status": drive.status

        })

    return jsonify(drive_list),200

@company_bp.route("/company/applicants/<int:drive_id>", methods=["GET"])
@jwt_required()
def view_applicants(drive_id):

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message":"Company not found"}),404

    drive = PlacementDrive.query.filter_by(
        id=drive_id,
        company_id=company.id
    ).first()

    if not drive:
        return jsonify({"message":"Drive not found"}),404

    applicants = Application.query.filter_by(
        drive_id=drive.id
    ).all()

    applicant_list = []

    for application in applicants:

        applicant_list.append({

            "application_id":application.id,
            "student_name":application.student.user.full_name,
            "email":application.student.user.email,
            "branch":application.student.branch,
            "cgpa":application.student.cgpa,
            "phone":application.student.phone,
            "has_resume": bool(application.student.resume),
            "status":application.status,
            "applied_at":application.applied_at.strftime("%Y-%m-%d")

        })

    return jsonify(applicant_list),200

@company_bp.route("/company/application/<int:application_id>/resume", methods=["GET"])
@jwt_required()
def view_applicant_resume(application_id):

    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    application = Application.query.get(application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    if application.drive.company_id != company.id:
        return jsonify({"message": "Access Denied"}), 403

    if not application.student.resume:
        return jsonify({"message": "Resume not uploaded"}), 404

    filepath = os.path.join("uploads", "resumes", application.student.resume)

    if not os.path.exists(filepath):
        return jsonify({"message": "Resume file not found"}), 404

    return send_file(
        filepath,
        mimetype="application/pdf",
        as_attachment=False
    )

@company_bp.route("/company/application/<int:id>/shortlist", methods=["PUT"])
@jwt_required()
def shortlist_applicant(id):
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    application = (
        Application.query
        .join(PlacementDrive)
        .filter(
            Application.id == id,
            PlacementDrive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"message": "Application not found"}), 404

    application.status = "Shortlisted"

    db.session.commit()

    return jsonify({"message": "Applicant Shortlisted"}), 200

@company_bp.route("/company/application/<int:id>/reject",methods=["PUT"])
@jwt_required()
def reject_applicant(id):
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    application = (
        Application.query
        .join(PlacementDrive)
        .filter(
            Application.id == id,
            PlacementDrive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"message": "Application not found"}), 404

    application.status = "Rejected"

    db.session.commit()

    return jsonify({"message": "Applicant Rejected"}), 200

@company_bp.route("/company/application/<int:id>/schedule", methods=["PUT"])
@jwt_required()
def schedule_interview(id):
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    application = (
        Application.query
        .join(PlacementDrive)
        .filter(
            Application.id == id,
            PlacementDrive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"message": "Application not found"}), 404

    data = request.get_json()

    application.status = "Interview"

    application.interview_date = datetime.strptime(
        data["interview_date"],
        "%Y-%m-%d %H:%M")

    db.session.commit()

    return jsonify({"message": "Interview Scheduled"}), 200

@company_bp.route("/company/application/<int:id>/offer",methods=["PUT"])
@jwt_required()
def offer_candidate(id):
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    application = (
        Application.query
        .join(PlacementDrive)
        .filter(
            Application.id == id,
            PlacementDrive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"message": "Application not found"}), 404

    application.status = "Offer"

    db.session.commit()

    return jsonify({"message": "Offer Released"}), 200

@company_bp.route("/company/application/<int:id>/place", methods=["PUT"])
@jwt_required()
def place_student(id):
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    application = (
        Application.query
        .join(PlacementDrive)
        .filter(
            Application.id == id,
            PlacementDrive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"message": "Application not found"}), 404

    existing_placement = Placement.query.filter_by(
        student_id=application.student_id,
        company_id=company.id
    ).first()

    if existing_placement:
        return jsonify({"message":"Student has already been marked as placed"}), 409

    application.status = "Placed"

    placement = Placement(
        student_id=application.student.id,
        company_id=company.id,
        position=application.drive.title,
        salary=application.drive.salary_package
    )

    db.session.add(placement)
    db.session.commit()

    return jsonify({"message": "Student Placed Successfully"}), 200

@company_bp.route("/company/application/<int:id>/status",methods=["PUT"])
@jwt_required()
def update_application_status(id):
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    application = (
        Application.query
        .join(PlacementDrive)
        .filter(
            Application.id == id,
            PlacementDrive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"message": "Application not found"}), 404

    data = request.get_json()

    allowed_status = [
        "Applied",
        "Shortlisted",
        "Interview",
        "Offer",
        "Rejected",
        "Placed"
    ]

    status = data.get("status")

    if status not in allowed_status:
        return jsonify({"message": "Invalid Status"}), 400

    application.status = status

    if data.get("feedback"):
        application.feedback = data.get("feedback")

    db.session.commit()

    return jsonify({"message": "Application Status Updated"}), 200

@company_bp.route("/company/application/<int:id>/feedback", methods=["PUT"])
@jwt_required()
def add_feedback(id):
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    application = (
        Application.query
        .join(PlacementDrive)
        .filter(
            Application.id == id,
            PlacementDrive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"message": "Application not found"}), 404

    data = request.get_json()

    application.feedback = data.get("feedback")

    db.session.commit()

    return jsonify({"message": "Feedback Added Successfully"}), 200