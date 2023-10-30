select
    t.fullname,
	sj.name as subject_name,
    round(avg(gd.grade), 2) AS average_grade
from grades gd
join subjects sj on sj.id = gd.subject_id
join teachers t on t.id = sj.teacher_id
where t.fullname = 'Камілла Вишняк'
group by t.fullname, sj.name;