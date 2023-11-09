import random
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session

fake = Faker('uk-UA')


def insert_data():
    for _ in range(3):
        group = Group(name=fake.word())
        session.add(group)
    for _ in range(3):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)
    for teacher in range(1, 4):
        for _ in range(2):
            subject = Subject(name=fake.word(), teacher_id=teacher)
            session.add(subject)
    for group_id in range(1, 4):
        for _ in range(10):
            student = Student(fullname=fake.name(), group_id=group_id)
            session.add(student)
            for subject in range(1, 7):
                for _ in range(3):
                    grade = Grade(student_id=student.id, subjects_id=subject, grade=random.randint(0, 100),
                                  grade_date=fake.date_this_decade())
                    session.add(grade)


if __name__ == '__main__':
    try:
        insert_data()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
