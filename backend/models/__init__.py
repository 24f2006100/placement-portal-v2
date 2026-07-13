from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password_hash=db.Column(db.String(255),nullable=False)
    role=db.Column(db.String(20),nullable=False)
    is_active=db.Column(db.Boolean,default=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    student=db.relationship("Student",back_populates="user",uselist=False,cascade="all,delete-orphan")
    company=db.relationship("Company",back_populates="user",uselist=False,cascade="all,delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"

class Student(db.Model):
    __tablename__="students"

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False,unique=True)
    branch=db.Column(db.String(100))
    cgpa=db.Column(db.Float)
    graduation_year=db.Column(db.Integer)
    phone=db.Column(db.String(20))
    resume=db.Column(db.String(255))

    user=db.relationship("User",back_populates="student")
    applications=db.relationship("Application",back_populates="student",cascade="all,delete-orphan")

class Company(db.Model):
    __tablename__="companies"

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False,unique=True)
    company_name=db.Column(db.String(150),nullable=False)
    website=db.Column(db.String(255))
    hr_name=db.Column(db.String(100))
    hr_email=db.Column(db.String(120))
    approval_status=db.Column(db.String(20),default="Pending")

    user=db.relationship("User",back_populates="company")
    drives=db.relationship("PlacementDrive",back_populates="company",cascade="all,delete-orphan")

class PlacementDrive(db.Model):
    __tablename__="placement_drives"

    id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer,db.ForeignKey("companies.id"),nullable=False)
    title=db.Column(db.String(150),nullable=False)
    description=db.Column(db.Text)
    salary_package=db.Column(db.Float)
    location=db.Column(db.String(100))
    branch_required=db.Column(db.String(100))
    cgpa_required=db.Column(db.Float)
    deadline=db.Column(db.Date)
    status=db.Column(db.String(20),default="Pending")

    company=db.relationship("Company",back_populates="drives")
    applications=db.relationship("Application",back_populates="drive",cascade="all,delete-orphan")

class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    salary = db.Column(db.Float)
    joining_date = db.Column(db.Date)

    student = db.relationship("Student")
    company = db.relationship("Company")

class Application(db.Model):
    __tablename__="applications"

    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)
    drive_id=db.Column(db.Integer,db.ForeignKey("placement_drives.id"),nullable=False)
    applied_at=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(30),default="Applied")
    interview_date = db.Column(db.DateTime, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    student=db.relationship("Student",back_populates="applications")
    drive=db.relationship("PlacementDrive",back_populates="applications")