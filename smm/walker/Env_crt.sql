drop table schedule.sessions;
create table schedule.sessions(
  session_id SERIAL not null,
  dt_start date,
  dt_stop date,
  client_key varchar(255)
);