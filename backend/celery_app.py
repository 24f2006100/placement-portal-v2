import csv
import os
from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from app import app
from models import *
from mail import send_email

celery = Celery(
    "placement_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
)

def write_csv(filename, headers, rows):

    os.makedirs("exports", exist_ok=True)

    filepath = os.path.join("exports", filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(headers)

        writer.writerows(rows)

    print(f"{filename} generated successfully")

    return filepath

@celery.task()
def export_students_csv():

    with app.app_context():

        students = Student.query.all()

        rows = []

        for student in students:

            rows.append([
                student.id,
                student.user.full_name,
                student.user.email,
                student.branch,
                student.cgpa,
                student.graduation_year,
                student.phone
            ])

        return write_csv(
            "students.csv",
            [
                "ID",
                "Name",
                "Email",
                "Branch",
                "CGPA",
                "Graduation Year",
                "Phone"
            ],
            rows
        )
    
@celery.task()
def export_companies_csv():

    with app.app_context():

        companies = Company.query.all()

        rows = []

        for company in companies:

            rows.append([
                company.id,
                company.company_name,
                company.user.email,
                company.hr_name,
                company.hr_email,
                company.website,
                company.approval_status
            ])

        return write_csv(
            "companies.csv",
            [
                "ID",
                "Company",
                "Email",
                "HR Name",
                "HR Email",
                "Website",
                "Status"
            ],
            rows
        )
    
@celery.task()
def export_applications_csv():

    with app.app_context():

        applications = Application.query.all()

        rows = []

        for application in applications:

            rows.append([
                application.id,
                application.student.user.full_name,
                application.drive.company.company_name,
                application.drive.title,
                application.status,
                application.applied_at.strftime("%Y-%m-%d %H:%M")
            ])

        return write_csv(
            "applications.csv",
            [
                "Application ID",
                "Student",
                "Company",
                "Drive",
                "Status",
                "Applied At"
            ],
            rows
        )
    
@celery.task()
def export_placements_csv():

    with app.app_context():

        placements = Placement.query.all()

        rows = []

        for placement in placements:

            rows.append([
                placement.id,
                placement.student.user.full_name,
                placement.company.company_name,
                placement.position,
                placement.salary,
                placement.joining_date
            ])

        return write_csv(
            "placements.csv",
            [
                "Placement ID",
                "Student",
                "Company",
                "Position",
                "Salary",
                "Joining Date"
            ],
            rows
        )
    
@celery.task()
def export_student_applications(student_id):

    with app.app_context():

        student = Student.query.get(student_id)

        if not student:
            return None

        applications = Application.query.filter_by(
            student_id=student_id
        ).all()

        rows = []

        for application in applications:

            rows.append([
                student.id,
                application.drive.company.company_name,
                application.drive.title,
                application.status,
                application.applied_at,
                application.interview_date
            ])

        filename = f"student_{student_id}_applications.csv"

        return write_csv(
            filename,
            [
                "Student ID",
                "Company Name",
                "Drive Title",
                "Application Status",
                "Applied At",
                "Interview Date"
            ],
            rows
        )
    
@celery.task()
def generate_monthly_activity_report():

    with app.app_context():

        # Previous month date range
        today = datetime.now()
        current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        previous_month_end = current_month - timedelta(days=1)
        previous_month_start = previous_month_end.replace(day=1)

        # Applications from previous month
        applications = Application.query.filter(
            Application.applied_at >= previous_month_start,
            Application.applied_at < current_month
        ).all()

        # Required statistics
        drives_conducted = len(set(app.drive_id for app in applications))

        students_applied = len(set(
            app.student_id for app in applications
        ))

        students_selected = len(set(
            app.student_id
            for app in applications
            if app.status == "Placed"
        ))

        month_name = previous_month_start.strftime("%B %Y")

        # HTML report content
        html_report = f"""
        <html>
        <body>
            <h2>Monthly Placement Activity Report</h2>

            <h3>{month_name}</h3>

            <p><b>Number of Drives Conducted:</b> {drives_conducted}</p>
            <p><b>Number of Students Applied:</b> {students_applied}</p>
            <p><b>Number of Students Selected:</b> {students_selected}</p>

            <p>
                This report was generated automatically
                by the Placement Portal.
            </p>
        </body>
        </html>
        """

        # Find Admin
        admin = User.query.filter_by(role="admin").first()

        if not admin:
            return "Admin not found"

        # Send HTML email
        send_email(
            admin.email,
            f"Monthly Placement Report - {month_name}",
            html_report,
            html=True
        )

        return f"Monthly report sent to {admin.email}"
    
@celery.task()
def daily_deadline_reminder():

    with app.app_context():

        today = datetime.now().date()

        reminder_limit = (
            today + timedelta(days=3)
        )

        upcoming_drives = (
            PlacementDrive.query
            .filter(
                PlacementDrive.status == "Approved",
                PlacementDrive.deadline >= today,
                PlacementDrive.deadline <= reminder_limit
            )
            .all()
        )

        students = Student.query.all()

        reminders_sent = 0

        for student in students:

            student_email = (
                student.user.email
            )

            student_name = (
                student.user.full_name
            )

            for drive in upcoming_drives:

                # Check whether the student
                # already applied to this drive

                existing_application = (
                    Application.query
                    .filter_by(
                        student_id=student.id,
                        drive_id=drive.id
                    )
                    .first()
                )

                # No need to remind students
                # who already applied

                if existing_application:
                    continue

                subject = (
                    "Placement Portal - "
                    "Upcoming Application Deadline"
                )

                body = f"""
Hello {student_name},

This is a reminder that the application deadline for an upcoming placement drive is approaching.

Company: {drive.company.company_name}
Position: {drive.title}
Location: {drive.location}
Salary Package: {drive.salary_package}
Required Branch: {drive.branch_required}
Minimum CGPA: {drive.cgpa_required}
Application Deadline: {drive.deadline}

Please log in to the Placement Portal and apply before the deadline if you are interested and eligible.

Best wishes,
Placement Portal
"""

                try:

                    send_email(
                        student_email,
                        subject,
                        body
                    )

                    reminders_sent += 1

                    print(
                        f"Deadline reminder sent to "
                        f"{student_email} for "
                        f"{drive.title}"
                    )


                except Exception as error:

                    print(
                        f"Failed to send reminder to "
                        f"{student_email}: {error}"
                    )


        return (
            f"Daily deadline reminders completed. "
            f"{reminders_sent} reminder(s) sent."
        )

celery.conf.beat_schedule = {

    "daily-deadline-reminder": {

        "task":
            "celery_app.daily_deadline_reminder",

        "schedule":crontab(hour=9, minute=0)
    },
    "monthly-activity-report": {

        "task": "celery_app.generate_monthly_activity_report",

        "schedule":crontab(day_of_month=1, hour=8, minute=0)
    }

}

