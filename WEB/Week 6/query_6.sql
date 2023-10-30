select
	st.fullname,
    g.name as group_name
from students st
join groups g on st.group_id = g.id
where g.name = 'modi'
group by st.fullname, g.name;