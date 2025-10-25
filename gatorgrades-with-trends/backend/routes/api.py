import csv, io
from flask import Blueprint, request
from sqlalchemy import func
from db import db
from models import Course, Assignment, Student, Grade, seed_demo

api_bp = Blueprint("api", __name__)

@api_bp.before_app_request
def ensure_seed():
    # Seed once per run
    if request.path.startswith("/api"):
        seed_demo(db.session)

@api_bp.get("/courses")
def list_courses():
    rows = Course.query.all()
    return {"courses": [{
        "id": c.id, "code": c.code, "title": c.title, "term": c.term
    } for c in rows]}

@api_bp.get("/courses/<int:course_id>/summary")
def course_summary(course_id):
    q = db.session.query(
        Course.id.label("course_id"),
        Course.code,
        func.count(func.distinct(Assignment.id)).label("assignments"),
        func.count(func.distinct(Grade.student_id)).label("students"),
        (func.avg(Grade.score / Assignment.max_score) * 100).label("avg_pct"),
        (func.percentile_cont(0.5).within_group((Grade.score / Assignment.max_score)) * 100).label("median_pct"),
        (func.stddev_pop(Grade.score / Assignment.max_score) * 100).label("stddev_pct"),
        (func.sum(func.case(( (Grade.score / Assignment.max_score) >= 0.6, 1), else_=0)) / func.count(Grade.id) * 100).label("pass_rate_pct")
    ).join(Assignment, Assignment.course_id == Course.id
    ).join(Grade, Grade.assignment_id == Assignment.id
    ).filter(Course.id == course_id
    ).group_by(Course.id, Course.code).first()

    if not q:
        return {"error": "not found"}, 404

    return {
        "course_id": q.course_id,
        "code": q.code,
        "assignments": int(q.assignments or 0),
        "students": int(q.students or 0),
        "avg_pct": float(q.avg_pct or 0),
        "median_pct": float(q.median_pct or 0),
        "stddev_pct": float(q.stddev_pct or 0),
        "pass_rate_pct": float(q.pass_rate_pct or 0),
    }

@api_bp.get("/courses/<int:course_id>/distribution")
def distribution(course_id):
    assignment_id = request.args.get("assignmentId", type=int)
    q = db.session.query(
        func.floor((Grade.score / Assignment.max_score) * 10).label("bucket"),
        func.count().label("count")
    ).join(Assignment, Assignment.id == Grade.assignment_id
    ).filter(Assignment.course_id == course_id)
    if assignment_id:
        q = q.filter(Assignment.id == assignment_id)
    q = q.group_by("bucket").order_by("bucket")

    buckets = [{"bucket": int(b or 0), "count": int(c)} for b, c in q]
    for i in range(0, 11):
        if not any(x["bucket"] == i for x in buckets):
            buckets.append({"bucket": i, "count": 0})
    buckets.sort(key=lambda x: x["bucket"])
    # Make labels like "0-10%", "10-20%", ...
    for x in buckets:
        lo = x["bucket"] * 10
        hi = min(100, (x["bucket"] + 1) * 10)
        x["bucketLabel"] = f"{lo}-{hi}%"
    return {"buckets": buckets}

@api_bp.post("/upload")
def upload_csv():
    if "file" not in request.files:
        return {"error": "file missing"}, 400
    file = request.files["file"]
    reader = csv.DictReader(io.StringIO(file.stream.read().decode()))
    upserts, new_grades = 0, 0
    for r in reader:
        course = Course.query.filter_by(code=r["course_code"], term=r["term"]).first()
        if not course:
            course = Course(code=r["course_code"], term=r["term"], title=r.get("course_title") or r["course_code"])
            db.session.add(course); db.session.flush()
        assign = Assignment.query.filter_by(course_id=course.id, title=r["assignment_title"]).first()
        if not assign:
            assign = Assignment(course_id=course.id, title=r["assignment_title"], max_score=r.get("max_score") or 100)
            db.session.add(assign); db.session.flush()
        student = Student.query.filter_by(external_id=r["student_external_id"]).first()
        if not student:
            student = Student(external_id=r["student_external_id"], name=r.get("student_name"))
            db.session.add(student); db.session.flush()
        g = Grade.query.filter_by(assignment_id=assign.id, student_id=student.id).first()
        if not g:
            g = Grade(assignment_id=assign.id, student_id=student.id, score=r["score"] or 0)
            db.session.add(g); new_grades += 1
        else:
            g.score = r["score"] or 0
        upserts += 1
    db.session.commit()
    return {"upserts": upserts, "new_grades": new_grades}


@api_bp.get("/courses/<int:course_id>/trends")
def trends(course_id):
    # Average percent per assignment, ordered by due_date (then id)
    rows = db.session.query(
        Assignment.id.label("assignment_id"),
        Assignment.title,
        Assignment.due_date,
        (func.avg(Grade.score / Assignment.max_score) * 100).label("avg_pct")
    ).join(Grade, Grade.assignment_id == Assignment.id
    ).filter(Assignment.course_id == course_id
    ).group_by(Assignment.id, Assignment.title, Assignment.due_date
    ).order_by(Assignment.due_date().asc() if hasattr(Assignment.due_date, '__call__') else Assignment.due_date.asc(), Assignment.id.asc()
    ).all()

    data = []
    for r in rows:
        data.append({
            "assignmentId": int(r.assignment_id),
            "title": r.title,
            "dueDate": r.due_date.isoformat() if r.due_date else None,
            "avg_pct": float(r.avg_pct or 0.0)
        })
    return {"trends": data}
