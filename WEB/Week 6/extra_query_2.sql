select
	sd.fullname as student_name,
	sj.name,
	gd.grade,
	gd.grade_date
from grades gd
join subjects sj on sj.id = gd.subject_id
join students sd on sd.id = gd.student_id
join groups gp on gp.id = sd.group_id
where sj.name = 'facere' and gp.name = 'blanditiis' and gd.grade_date = (select max(grade_date) from grades)
group by sd.fullname, sj.name, gd.grade, gd.grade_date
