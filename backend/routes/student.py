from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models import *
from extensions import db
from cache_config import cache
import os
from flask import send_file
from celery.result import AsyncResult
from werkzeug.utils import secure_filename

student_bp = Blueprint("student", __name__)

RESUME_FOLDER = "uploads/resumes"
os.makedirs(
    RESUME_FOLDER,
    exist_ok=True
)

@student_bp.route("/student/dashboard", methods=["GET"])
@jwt_required()
def student_dashboard():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message":"Student not found"}),404

    dashboard = {
        "full_name": student.user.full_name,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "resume": student.resume,
        "total_applications": Application.query.filter_by(student_id=student.id).count()
    }

    return jsonify(dashboard),200

@student_bp.route("/student/drives", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def get_available_drives():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message":"Access Denied"}),403

    student_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=student_id).first()

    if not student:
        return jsonify({"message":"Student not found"}),404

    drives = PlacementDrive.query.filter_by(status="Approved").all()

    drive_list = []

    for drive in drives:

        drive_list.append({

            "id":drive.id,
            "company":drive.company.company_name,
            "title":drive.title,
            "description":drive.description,
            "salary_package":drive.salary_package,
            "location":drive.location,
            "branch_required":drive.branch_required,
            "cgpa_required":drive.cgpa_required,
            "deadline":drive.deadline.strftime("%Y-%m-%d")

        })

    return jsonify(drive_list),200

@student_bp.route("/student/apply/<int:drive_id>", methods=["POST"])
@jwt_required()
def apply_drive(drive_id):

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message":"Student not found"}),404

    drive = PlacementDrive.query.filter_by(id=drive_id, status="Approved").first()

    if not drive:
        return jsonify({"message":"Drive not found or not available"}), 404
    
    if (drive.cgpa_required is not None and 
        (
        student.cgpa is None
        or student.cgpa < drive.cgpa_required
        )
    ):
        return jsonify({
        "message": f"Minimum CGPA required is {drive.cgpa_required}"}), 403

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id).first()

    if existing:
        return jsonify({"message":"Already Applied"}),409

    application = Application(
        student_id=student.id,
        drive_id=drive.id
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message":"Applied Successfully"}),201

@student_bp.route("/student/applications", methods=["GET"])
@jwt_required()
def my_applications():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message":"Student not found"}),404

    applications = Application.query.filter_by(student_id=student.id).all()

    application_list = []

    for application in applications:

        application_list.append({
            "application_id": application.id,
            "company":application.drive.company.company_name,
            "title":application.drive.title,
            "status":application.status,
            "feedback":application.feedback,
            "interview_date":
                application.interview_date.strftime("%Y-%m-%d %H:%M")
                if application.interview_date else None,
            "applied_at":
                application.applied_at.strftime("%Y-%m-%d")

})

    return jsonify(application_list),200

@student_bp.route("/student/application/<int:id>", methods=["DELETE"])
@jwt_required()
def withdraw_application(id):

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    application = Application.query.filter_by(
        id=id,
        student_id=student.id
    ).first()

    if not application:
        return jsonify({"message":"Application not found"}),404

    db.session.delete(application)
    db.session.commit()

    return jsonify({"message":"Application Withdrawn Successfully"}),200

@student_bp.route("/student/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message":"Access Denied"}),403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message":"Student not found"}),404

    data = request.get_json()

    student.branch = data.get("branch",student.branch)
    student.cgpa = data.get("cgpa",student.cgpa)
    student.graduation_year = data.get("graduation_year",student.graduation_year)
    student.phone = data.get("phone",student.phone)

    db.session.commit()

    return jsonify({"message":"Profile Updated Successfully"}),200

@student_bp.route("/student/interviews", methods=["GET"])
@jwt_required()
def interview_schedule():

    claims=get_jwt()

    if claims["role"]!="student":
        return jsonify({"message":"Access Denied"}),403

    user_id=int(get_jwt_identity())

    student=Student.query.filter_by(user_id=user_id).first()

    applications=Application.query.filter_by(student_id=student.id).all()

    interview_list=[]

    for application in applications:

        if application.interview_date:

            interview_list.append({

                "company":application.drive.company.company_name,
                "drive":application.drive.title,
                "interview_date":application.interview_date.strftime("%Y-%m-%d %H:%M"),
                "status":application.status

            })

    return jsonify(interview_list),200

@student_bp.route("/student/search/drives", methods=["GET"])
@jwt_required()
def search_drives():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message":"Access Denied"}),403

    title = request.args.get("title","")

    drives = PlacementDrive.query.filter(
        PlacementDrive.status=="Approved",
        PlacementDrive.title.ilike(f"%{title}%")
    ).all()

    result=[]

    for drive in drives:

        result.append({
            "id": drive.id,
            "company": drive.company.company_name,
            "title": drive.title,
            "description": drive.description,
            "salary_package": drive.salary_package,
            "location": drive.location,
            "branch_required": drive.branch_required,
            "cgpa_required": drive.cgpa_required,
            "deadline": drive.deadline.strftime("%Y-%m-%d")
        })

    return jsonify(result),200

@student_bp.route("/student/export/applications",methods=["POST"])
@jwt_required()
def export_applications():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    from celery_app import (
        export_student_applications
    )

    task = export_student_applications.delay(
        student.id
    )

    return jsonify({"message": "Export started","task_id": task.id}), 202

@student_bp.route("/student/export/status/<task_id>",methods=["GET"])
@jwt_required()
def export_status(task_id):
    from celery_app import celery

    task = AsyncResult(
        task_id,
        app=celery
    )

    if task.state == "SUCCESS":
        return jsonify({
            "status": "SUCCESS",
            "filename": os.path.basename(
                task.result
            )
        }), 200

    if task.state == "FAILURE":
        return jsonify({"status": "FAILURE"}), 500

    return jsonify({"status": task.state}), 200

@student_bp.route("/student/export/download/<filename>",methods=["GET"])
@jwt_required()
def download_student_export(filename):

    filepath = os.path.join(
        "exports",
        filename
    )

    if not os.path.exists(filepath):
        return jsonify({"message": "Export file not found"}), 404

    return send_file(
        filepath,
        as_attachment=True
    )

@student_bp.route("/student/resume",methods=["POST"])
@jwt_required()
def upload_resume():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    if "resume" not in request.files:
        return jsonify({"message": "No resume file selected"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"message": "No resume file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"message": "Only PDF files are allowed"}), 400

    filename = secure_filename(
        f"student_{student.id}_resume.pdf"
    )


    filepath = os.path.join(
        RESUME_FOLDER,
        filename
    )

    file.save(filepath)

    student.resume = filename

    db.session.commit()

    return jsonify({"message": "Resume uploaded successfully","resume": filename}), 200

@student_bp.route("/student/resume",methods=["GET"])
@jwt_required()
def view_resume():

    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access Denied"}), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()


    if not student or not student.resume:
        return jsonify({"message": "Resume not found"}), 404

    filepath = os.path.join(
        RESUME_FOLDER,
        student.resume
    )

    if not os.path.exists(filepath):
        return jsonify({"message": "Resume file not found"}), 404

    return send_file(
        filepath,
        mimetype="application/pdf",
        as_attachment=False
    )