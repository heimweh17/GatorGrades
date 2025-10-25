import io
import csv

def test_health(client):
    rv = client.get('/api/health')
    assert rv.status_code == 200
    assert rv.get_json()['status'] == 'ok'

def test_upload_and_summary(client):
    # Build a minimal CSV in-memory
    csv_data = """course_code,term,assignment_title,student_external_id,student_name,score,max_score,graded_at
COP3530,Fall 2025,HW1,12345678,Alex Liu,90,100,2025-09-11
COP3530,Fall 2025,HW1,87654321,Ben Zhang,80,100,2025-09-11
COP3530,Fall 2025,Quiz1,12345678,Alex Liu,45,50,2025-09-18
COP3530,Fall 2025,Quiz1,87654321,Ben Zhang,40,50,2025-09-18
"""
    data = {'file': (io.BytesIO(csv_data.encode()), 'grades.csv')}
    rv = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200
    j = rv.get_json()
    assert j['upserts'] == 4
    assert j['new_grades'] == 4

    # Fetch courses and pick the first
    rv = client.get('/api/courses')
    assert rv.status_code == 200
    courses = rv.get_json()['courses']
    assert len(courses) == 1
    course_id = courses[0]['id']

    # Get summary and check aggregates roughly
    rv = client.get(f'/api/courses/{course_id}/summary')
    assert rv.status_code == 200
    s = rv.get_json()
    # 2 assignments, 2 students
    assert s['assignments'] == 2
    assert s['students'] == 2
    # Average percent should be around 85% ( (90+80)/200 + (45+40)/100 ) / 2 * 100 = 85
    assert abs(s['avg_pct'] - 85.0) < 1e-6

def test_distribution_buckets(client):
    # Reuse sample CSV for more buckets
    sample = """course_code,term,assignment_title,assignment_due,student_external_id,student_name,score,max_score,graded_at
COP3530,Fall 2025,HW1,2025-09-10,12345678,Alex Liu,92,100,2025-09-11
COP3530,Fall 2025,HW1,2025-09-10,87654321,Ben Zhang,81,100,2025-09-11
COP3530,Fall 2025,Quiz1,2025-09-17,12345678,Alex Liu,45,50,2025-09-18
COP3530,Fall 2025,Quiz1,2025-09-17,87654321,Ben Zhang,39,50,2025-09-18
COP3530,Fall 2025,HW2,2025-09-24,12345678,Alex Liu,88,100,2025-09-25
COP3530,Fall 2025,HW2,2025-09-24,87654321,Ben Zhang,74,100,2025-09-25
"""
    data = {'file': (io.BytesIO(sample.encode()), 'grades.csv')}
    rv = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200

    # Find the course
    rv = client.get('/api/courses')
    course_id = rv.get_json()['courses'][0]['id']

    # Distribution should return 0..10 buckets with non-negative counts
    rv = client.get(f'/api/courses/{course_id}/distribution')
    buckets = rv.get_json()['buckets']
    assert len(buckets) == 11
    assert all('bucket' in b and 'count' in b for b in buckets)
    assert all(0 <= b['bucket'] <= 10 for b in buckets)
