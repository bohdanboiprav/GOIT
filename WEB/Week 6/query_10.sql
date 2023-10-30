select
	sd.fullname as student_name,
	t.fullname as teacher_name,
	sj.name as subject_name
from subjects sj
join grades gd on sj.id = gd.subject_id
join students sd on sd.id = gd.student_id
join teachers t on t.id = sj.teacher_id
where sd.fullname = 'Семен Щорс' and t.fullname = 'Камілла Вишняк'
group by sd.fullname, sj.name, t.fullname;