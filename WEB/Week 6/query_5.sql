select
	t.fullname,
    s.name as subject
from teachers t
join subjects s on s.teacher_id = t.id
where t.fullname = 'Камілла Вишняк'
group by t.fullname, s.name;