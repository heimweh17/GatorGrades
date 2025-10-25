from db import db
from sqlalchemy import func, CheckConstraint

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    term = db.Column(db.String, nullable=False)

    assignments = db.relationship("Assignment", backref="course", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint('code', 'term', name='uq_course_code_term'),
    )

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String)

    __table_args__ = (
        db.UniqueConstraint('external_id', name='uq_student_external'),
    )

class Assignment(db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date)
    max_score = db.Column(db.Numeric(6,2), nullable=False)

    grades = db.relationship("Grade", backref="assignment", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("max_score > 0", name="ck_max_score_positive"),
    )

class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # <-- critical
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_id    = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    score         = db.Column(db.Numeric(6,2), nullable=False)
    graded_at     = db.Column(db.Date)
    __table_args__ = (
        db.UniqueConstraint('assignment_id', 'student_id', name='uq_grade_per_assignment'),
        db.CheckConstraint("score >= 0", name="ck_score_nonnegative"),
    )


def seed_demo(db_session):
    # Quick seed to verify charts
    if not Course.query.first():
        c = Course(code="COP3530", title="Data Structures & Algorithms", term="Fall 2025")
        db_session.add(c)
        db_session.flush()
        from datetime import date
        a1 = Assignment(course_id=c.id, title="HW1", due_date=date(2025,9,10), max_score=100)
        a2 = Assignment(course_id=c.id, title="Quiz1", due_date=date(2025,9,17), max_score=50)
        db_session.add_all([a1, a2]); db_session.flush()
        s1 = Student(external_id="12345678", name="Alex Liu")
        s2 = Student(external_id="87654321", name="Ben Zhang")
        db_session.add_all([s1, s2]); db_session.flush()
        g1 = Grade(assignment_id=a1.id, student_id=s1.id, score=92, graded_at=date(2025,9,11))
        g2 = Grade(assignment_id=a1.id, student_id=s2.id, score=81, graded_at=date(2025,9,11))
        g3 = Grade(assignment_id=a2.id, student_id=s1.id, score=45, graded_at=date(2025,9,18))
        g4 = Grade(assignment_id=a2.id, student_id=s2.id, score=39, graded_at=date(2025,9,18))
        db_session.add_all([g1, g2, g3, g4])
        db_session.commit()
