drop table schedule.source_names;
create table schedule.source_names(
    source_id integer,
    source_name varchar(100)
);

drop table schedule.act_periods;
create table schedule.act_periods(
    act_period_id integer,
    act_period_name  varchar(100)
);

drop table schedule.schedule_bot_action;
create table schedule.schedule_bot_action(
    act_period integer,
    date_mask date,
    time_mask time,
    bot_class_name varchar(100),
    bot_params text
);

GRANT ALL ON ALL TABLES IN SCHEMA social TO etl;
commit;

select nextval('social.bot_log_bot_log_id');
