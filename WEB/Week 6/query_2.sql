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
