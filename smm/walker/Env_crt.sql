drop table schedule.sessions;
commit;

create table schedule.sessions(
  session_id SERIAL not null,
  dt_start date,
  dt_stop date,
  client_key varchar(255)
);

create table schedule.session_variable(
  variable_key varchar(64) not null,
  session_id integer,
  int_value integer,
  varchar_value varchar(100)
);

delete from schedule.executed_bot_action t where t.exe_date > to_date('02 Feb 2019', 'DD Mon YYYY');