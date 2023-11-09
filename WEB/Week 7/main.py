from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_01():
    """
    select
        s.id,
        s.fullname,
        round(avg(g.grade), 2) AS average_grade
    from students s
    join grades g on s.id = g.student_id
    group by s.id
    order by average_grade desc
    limit 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    """
    select
        s.id,
        s.fullname,
        sb.name as subject,
        round(avg(g.grade), 2) AS average_grade
    from grades g
    join students s on s.id = g.student_id
    join subjects sb on sb.id = g.subject_id
    where sb.name = 'laborum'
    group by s.id, sb.name
    order by average_grade desc
    limit 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


def select_03():
    """
    select
        gp.name as Group_Name,
        sb.name as subject,
        round(avg(g.grade), 2) AS average_grade
    from grades g
    join students s on s.id = g.student_id
    join subjects sb on sb.id = g.subject_id
    join groups gp on s.group_id = gp.id
    where sb.name = 'ullam'
    group by sb.name, gp.name
    order by average_grade desc;
    """
    result = session.query(Group.name.label('Group_Name'), Subject.name.label('subject'),
                           func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).join(Subject).join(Group).filter(Subject.name == 'ullam').group_by(
        Subject.name, Group.name).order_by(
        desc('average_grade')).all()
    return result


def select_04():
    """
    select
        round(avg(g.grade), 2) AS average_grade
    from grades g
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).all()
    return result


def select_05():
    """
    select
        t.fullname,
        s.name as subject
    from teachers t
    join subjects s on s.teacher_id = t.id
    where t.fullname = 'Едита Цюпа'
    group by t.fullname, s.name;
    """
    result = session.query(Teacher.fullname, Subject.name.label('subject')) \
        .select_from(Teacher).join(Subject).filter(Teacher.fullname == 'Едита Цюпа').group_by(
        Teacher.fullname, Subject.name).all()
    return result


def select_06():
    """
    select
        st.fullname,
        g.name as group_name
    from students st
    join groups g on st.group_id = g.id
    where g.name = 'beatae'
    group by st.fullname, g.name;
    """
    result = session.query(Student.fullname, Group.name.label('group_name')) \
        .select_from(Student).join(Group).filter(Group.name == 'beatae').group_by(
        Student.fullname, Group.name).all()
    return result


def select_07():
    """
    select
        gd.grade,
        gd.grade_date,
        sj.name as subject_name,
        g.name as group_name
    from grades gd
    join students st on st.id = gd.student_id
    join groups g on st.group_id = g.id
    join subjects sj on sj.id = gd.subject_id
    where g.name = 'beatae' and sj.name = 'blanditiis'
    group by gd.grade, gd.grade_date, sj.name, st.fullname, g.name;
    """
    result = session.query(Grade.grade, Grade.grade_date, Subject.name.label('subject_name'),
                           Group.name.label('group_name')) \
        .select_from(Grade).join(Student).join(Group).join(Subject).filter(Group.name == 'beatae',
                                                                           Subject.name == 'blanditiis').group_by(
        Grade.grade, Grade.grade_date, Subject.name, Student.fullname, Group.name).all()
    return result


def select_08():
    """
    select
        t.fullname,
        sj.name as subject_name,
        round(avg(gd.grade), 2) AS average_grade
    from grades gd
    join subjects sj on sj.id = gd.subject_id
    join teachers t on t.id = sj.teacher_id
    where t.fullname = 'Едита Цюпа'
    group by t.fullname, sj.name;
    """
    result = session.query(Teacher.fullname, Subject.name.label('subject_name'),
                           func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Subject).join(Teacher).filter(Teacher.fullname == 'Едита Цюпа').group_by(
        Teacher.fullname, Subject.name).all()
    return result


def select_09():
    """
    select
        sd.fullname,
        sj.name as subject_name
    from subjects sj
    join grades gd on sj.id = gd.subject_id
    join students sd on sd.id = gd.student_id
    where sd.fullname = 'Макар Гресь'
    group by sd.fullname, sj.name;
    """
    result = session.query(Student.fullname, Subject.name.label('subject_name')) \
        .select_from(Subject).join(Grade).join(Student).filter(Student.fullname == 'Макар Гресь').group_by(
        Student.fullname, Subject.name).all()
    return result


def select_10():
    """
    select
        sd.fullname as student_name,
        t.fullname as teacher_name,
        sj.name as subject_name
    from subjects sj
    join grades gd on sj.id = gd.subject_id
    join students sd on sd.id = gd.student_id
    join teachers t on t.id = sj.teacher_id
    where sd.fullname = 'Макар Гресь' and t.fullname = 'Едита Цюпа'
    group by sd.fullname, sj.name, t.fullname;
    """
    result = session.query(Student.fullname.label('student_name'), Teacher.fullname.label('teacher_name'),
                           Subject.name.label('subject_name')) \
        .select_from(Subject).join(Grade).join(Student).join(Teacher).filter(
        Student.fullname == 'Макар Гресь', Teacher.fullname == 'Едита Цюпа').group_by(
        Student.fullname, Subject.name, Teacher.fullname).all()
    return result


def select_11():
    """
    select
        sd.fullname as student_name,
        t.fullname as teacher_name,
        round(avg(gd.grade), 2) AS average_grade
    from grades gd
    join subjects sj on sj.id = gd.subject_id
    join students sd on sd.id = gd.student_id
    join teachers t on t.id = sj.teacher_id
    where sd.fullname = 'Макар Гресь' and t.fullname = 'Едита Цюпа'
    group by sd.fullname, t.fullname;
    """
    result = session.query(Student.fullname.label('student_name'), Teacher.fullname.label('teacher_name'),
                           func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Subject).join(Student).join(Teacher).filter(
        Student.fullname == 'Макар Гресь', Teacher.fullname == 'Едита Цюпа').group_by(
        Student.fullname, Teacher.fullname).all()
    return result


def select_12():
    """
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 2 and s.group_id  =3;

    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 2 and s.group_id = 3 and g.grade_date = (
        select max(grade_date)
        from grades g2
        join students s2 on s2.id=g2.student_id
        where g2.subject_id = 2 and s2.group_id = 3
    );
    :return:
    """

    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subjects_id == 2, Student.group_id == 3
    ))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.grade_date == subquery)).all()

    return result


if __name__ == '__main__':
    print(select_01())
    print(select_02())
    print(select_03())
    print(select_04())
    print(select_05())
    print(select_06())
    print(select_07())
    print(select_08())
    print(select_09())
    print(select_10())
    print(select_11())
    print(select_12())
