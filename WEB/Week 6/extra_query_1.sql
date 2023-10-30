select
	sd.fullname as student_name,
	t.fullname as teacher_name,
	round(avg(gd.grade), 2) AS average_grade
from grades gd
join subjects sj on sj.id = gd.subject_id
join students sd on sd.id = gd.student_id
join teachers t on t.id = sj.teacher_id
where sd.fullname = 'Семен Щорс' and t.fullname = 'Камілла Вишняк'
group by sd.fullname, t.fullname;