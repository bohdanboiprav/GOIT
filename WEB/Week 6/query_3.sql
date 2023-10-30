select
	gp.name as Group_Name,
    sb.name as subject,
    round(avg(g.grade), 2) AS average_grade
from grades g
join students s on s.id = g.student_id
join subjects sb on sb.id = g.subject_id
join groups gp on s.group_id = gp.id
where sb.name = 'laborum'
group by sb.name, gp.name
order by average_grade desc;