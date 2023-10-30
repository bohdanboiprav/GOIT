select
	gd.grade,
	gd.grade_date,
	sj.name as subject_name,
    g.name as group_name
from grades gd
join students st on st.id = gd.student_id
join groups g on st.group_id = g.id
join subjects sj on sj.id = gd.subject_id
where g.name = 'modi' and sj.name = 'facere'
group by gd.grade, gd.grade_date, sj.name, st.fullname, g.name;
