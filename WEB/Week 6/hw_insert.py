import random
import logging
from faker import Faker
from psycopg2 import DatabaseError
from connection import create_connection

fake = Faker('uk-UA')

with create_connection() as conn:
    cur = conn.cursor()
    for _ in range(3):
        cur.execute("INSERT INTO groups (name) VALUES (%s)", (fake.word(),))

    for _ in range(3):
        cur.execute("INSERT INTO teachers (fullname) VALUES (%s)", (fake.name(),))

    for teacher_id in range(1, 4):
        for _ in range(2):
            cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s)", (fake.word(), teacher_id))

    for group_id in range(1, 4):
        for _ in range(10):
            cur.execute("INSERT INTO students (fullname, group_id) VALUES (%s, %s) RETURNING id",
                        (fake.name(), group_id))
            student_id = cur.fetchone()[0]
            for subject_id in range(1, 7):
                for _ in range(3):
                    cur.execute(
                        "INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)",
                        (student_id, subject_id, random.randint(0, 100), fake.date_this_decade()))
    try:
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
