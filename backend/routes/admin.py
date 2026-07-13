from flask import Blueprint, jsonify,request,send_file
from flask_jwt_extended import jwt_required, get_jwt
from models import *
from extensions import db
from cache_config import cache

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403

    dashboard = {
        "total_students": Student.query.count(),
        "total_companies": Company.query.count(),
        "pending_companies": Company.query.filter_by(approval_status="Pending").count(),
        "approved_companies": Company.query.filter_by(approval_status="Approved").count(),
        "total_drives": PlacementDrive.query.count(),
        "total_applications": Application.query.count()
    }

    return jsonify(dashboard), 200

@admin_bp.route("/admin/companies", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def get_companies():
    
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    companies = Company.query.all()

    company_list = []

    for company in companies:

        company_list.append({
            "id": company.id,
            "company_name": company.company_name,
            "email": company.user.email,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "website": company.website,
            "approval_status": company.approval_status,
            "is_active": company.user.is_active
        })

    return jsonify(company_list),200

@admin_bp.route("/admin/company/<int:id>/approve", methods=["PUT"])
@jwt_required()
def approve_company(id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    company = Company.query.get(id)

    if not company:
        return jsonify({"message":"Company not found"}),404

    company.approval_status = "Approved"

    db.session.commit()
    cache.clear()

    return jsonify({"message":"Company Approved Successfully"}),200

@admin_bp.route("/admin/company/<int:id>/reject", methods=["PUT"])
@jwt_required()
def reject_company(id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    company = Company.query.get(id)

    if not company:
        return jsonify({"message":"Company not found"}),404

    company.approval_status = "Rejected"

    db.session.commit()
    cache.clear()

    return jsonify({"message":"Company Rejected Successfully"}),200

@admin_bp.route("/admin/students", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def get_students():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    students = Student.query.all()

    student_list = []

    for student in students:

        student_list.append({
            "id": student.id,
            "full_name": student.user.full_name,
            "email": student.user.email,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "phone": student.phone,
            "is_active": student.user.is_active
        })

    return jsonify(student_list),200

@admin_bp.route("/admin/drives", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def get_drives():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    drives = PlacementDrive.query.all()

    drive_list = []

    for drive in drives:

        drive_list.append({

            "id":drive.id,
            "company":drive.company.company_name,
            "title":drive.title,
            "location":drive.location,
            "salary_package":drive.salary_package,
            "branch_required":drive.branch_required,
            "cgpa_required":drive.cgpa_required,
            "deadline":drive.deadline.strftime("%Y-%m-%d"),
            "status":drive.status

        })

    return jsonify(drive_list),200

@admin_bp.route("/admin/drive/<int:id>/approve",methods=["PUT"])
@jwt_required()
def approve_drive(id):

    claims=get_jwt()

    if claims["role"]!="admin":
        return jsonify({"message":"Access Denied"}),403

    drive=PlacementDrive.query.get(id)

    if not drive:
        return jsonify({"message":"Drive not found"}),404

    drive.status="Approved"

    db.session.commit()
    cache.clear()

    return jsonify({"message":"Drive Approved"}),200

@admin_bp.route("/admin/drive/<int:id>/reject",methods=["PUT"])
@jwt_required()
def reject_drive(id):

    claims=get_jwt()

    if claims["role"]!="admin":
        return jsonify({"message":"Access Denied"}),403

    drive=PlacementDrive.query.get(id)

    if not drive:
        return jsonify({"message":"Drive not found"}),404

    drive.status="Rejected"
    cache.clear()

    db.session.commit()

    return jsonify({"message":"Drive Rejected"}),200

@admin_bp.route("/admin/drive/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_drive_admin(id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    drive = PlacementDrive.query.get(id)

    if not drive:
        return jsonify({"message":"Drive not found"}),404

    db.session.delete(drive)
    db.session.commit()
    cache.clear()

    return jsonify({"message":"Drive Deleted"}),200

@admin_bp.route("/admin/applications", methods=["GET"])
@jwt_required()
def get_all_applications():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    applications = Application.query.all()

    application_list = []

    for application in applications:

        application_list.append({

            "id":application.id,
            "student":application.student.user.full_name,
            "company":application.drive.company.company_name,
            "drive":application.drive.title,
            "status":application.status,
            "applied_at":application.applied_at.strftime("%Y-%m-%d"),
            "interview_date":application.interview_date.strftime("%Y-%m-%d %H:%M") if application.interview_date else None,
            "feedback":application.feedback

        })

    return jsonify(application_list),200

@admin_bp.route("/admin/application/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_application(id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    application = Application.query.get(id)

    if not application:
        return jsonify({"message":"Application not found"}),404

    db.session.delete(application)
    db.session.commit()

    return jsonify({"message":"Application Deleted"}),200

@admin_bp.route("/admin/search/company", methods=["GET"])
@jwt_required()
def search_company():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    name = request.args.get("name","")

    companies = Company.query.filter(
        Company.company_name.ilike(f"%{name}%")
    ).all()

    result = []

    for company in companies:

        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "email": company.user.email,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "website": company.website,
            "approval_status": company.approval_status
        })

    return jsonify(result),200

@admin_bp.route("/admin/search/student", methods=["GET"])
@jwt_required()
def search_student():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    name = request.args.get("name","")

    students = Student.query.join(User).filter(
        User.full_name.ilike(f"%{name}%")
    ).all()

    result = []

    for student in students:

        result.append({

            "id":student.id,
            "name":student.user.full_name,
            "email":student.user.email,
            "branch":student.branch,
            "cgpa":student.cgpa,
            "graduation_year":student.graduation_year,
            "phone": student.phone

        })

    return jsonify(result),200

@admin_bp.route("/admin/company/<int:id>/deactivate", methods=["PUT"])
@jwt_required()
def deactivate_company(id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    company = Company.query.get(id)

    if not company:
        return jsonify({"message":"Company not found"}),404

    company.user.is_active = False

    db.session.commit()
    cache.clear()

    return jsonify({"message":"Company Deactivated"}),200

@admin_bp.route("/admin/student/<int:id>/deactivate", methods=["PUT"])
@jwt_required()
def deactivate_student(id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    student = Student.query.get(id)

    if not student:
        return jsonify({"message":"Student not found"}),404

    student.user.is_active = False

    db.session.commit()
    cache.clear()

    return jsonify({"message":"Student Deactivated"}),200

@admin_bp.route("/admin/export/students", methods=["GET"])
@jwt_required()
def export_students():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    from celery_app import export_students_csv

    export_students_csv.delay()

    return jsonify({"message":"Student CSV export started."}),200

@admin_bp.route("/admin/export/companies", methods=["GET"])
@jwt_required()
def export_companies():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    from celery_app import export_companies_csv

    export_companies_csv.delay()

    return jsonify({"message":"Company CSV export started."}),200

@admin_bp.route("/admin/export/applications", methods=["GET"])
@jwt_required()
def export_applications():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    from celery_app import export_applications_csv

    export_applications_csv.delay()

    return jsonify({"message":"Applications CSV export started."}),200

@admin_bp.route("/admin/export/placements", methods=["GET"])
@jwt_required()
def export_placements():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message":"Access Denied"}),403

    from celery_app import export_placements_csv

    export_placements_csv.delay()

    return jsonify({"message":"Placements CSV export started."}),200

@admin_bp.route("/admin/download/<filename>", methods=["GET"])
@jwt_required()
def download_file(filename):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access Denied"}), 403

    return send_file(f"exports/{filename}",as_attachment=True)
