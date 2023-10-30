create table students (
	id SERIAL primary key,
	fullname varchar(200) not null,
	group_id integer references group(id)
		on delete cascade
);

create table groups (
	id SERIAL primary key,
	name varchar(70) not null
);

create table teachers (
	id SERIAL primary key,
	fullname varchar(200) not null
);

create table subjects (
  id SERIAL primary key,
  name varchar(175) not null,
  teacher_id integer  references teachers(id)
  	on delete cascade
);

create table grades (
  id SERIAL primary key,
  student_id integer references students(id)
  on delete cascade,
  subject_id integer references subjects(id)
  on delete cascade,
  grade integer check (grade >= 0 AND grade <= 100),
  grade_date date not null
);