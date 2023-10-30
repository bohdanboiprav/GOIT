select 
    s.id, 
    s.fullname, 
    round(avg(g.grade), 2) AS average_grade
from students s
join grades g on s.id = g.student_id
group by s.id
order by average_grade desc
limit 5;