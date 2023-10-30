select
	sd.fullname,
	sj.name as subject_name
from subjects sj
join grades gd on sj.id = gd.subject_id
join students sd on sd.id = gd.student_id
where sd.fullname = 'Семен Щорс'
group by sd.fullname, sj.name;